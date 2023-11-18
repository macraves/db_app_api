"""user related routes"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from allwebforms import UserForm, LoginForm
from data_models import db, User

# Create blueprints connection
user_bp = Blueprint("user", __name__, url_prefix="/users", template_folder="templates")


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    """Login route for the users."""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            login_user(user)
            flash(f"{username} logged in successfully")
            return redirect(url_for("user.users_all"))
        flash("Invalid username or password. Try again!")
    return render_template("user.user_login.html", header="Login", form=form)


@user_bp.route("/logout")
@login_required
def logout():
    """Logout route for the users."""
    logout_user()
    flash(f"{current_user.username} logged out successfully")
    return redirect(url_for("user.login"))


@user_bp.route("/all")
def users_all():
    """Users page"""
    users = User.query.all()
    return render_template("users_all.html", header="All Users", users=users)


@user_bp.route("/add", methods=["GET", "POST"])
def user_add():
    """Add user"""
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data.title().strip(),
            username=form.username.data.strip(),
            email=form.email.data.strip(),
            password=form.password1.data.strip(),
        )
        if user is None or not user.verify_password(form.password1.data.strip()):
            flash("Invalid username or password")
            return render_template("user_add.html", header="Add User", form=form)
        db.session.add(user)
        db.session.commit()
        flash(f"<strong>{form.username.data}</strong> has been added")
        form.name.data = ""
        form.username.data = ""
        form.email.data = ""
        form.password1.data = ""
        form.password2.data = ""
        return redirect("/users")
    return render_template("user_add.html", header="Add User", form=form)


@user_bp.route("/user/update/<int:user_id>/", methods=["GET", "POST"])
def user_update(user_id):
    """Update user"""
    user = User.query.get_or_404(user_id)
    if user is None:
        flash("User not found")
        return redirect("/users")
    form = UserForm(obj=user)
    if request.method == "POST":
        user.name = request.form.get("name").title().strip()
        user.username = request.form.get("username").strip()
        user.email = request.form.get("email").strip()
        db.session.commit()
        flash(f"<strong>{form.username.data}</strong> has been updated")
        return redirect(url_for("user.users_all"))
    return render_template(
        "user_update.html", header="Update User", form=form, user_id=user_id
    )


@user_bp.route("/user/delete/<int:user_id>/", methods=["GET", "POST"])
def user_delete(user_id):
    """Delete user"""
    user = User.query.get_or_404(user_id)
    if user is None:
        flash("User not found")
        return redirect("/users")
    db.session.delete(user)
    db.session.commit()
    flash(f"<strong>{user.username}</strong> has been deleted")
    return redirect("/users")
