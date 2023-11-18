"""Flask app for database, create its database extension, and create its table."""
from datetime import datetime
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_migrate import Migrate
from flask_login import (
    current_user,
    LoginManager,
    login_user,
    logout_user,
    login_required,
)
from allwebforms import BookForm, UserForm, PostForm, PasswordForm, LoginForm
from data_models import db, User, Book, Post, MYSQL_URI

app = Flask(__name__)
# Create sqlite3 library.db by defined file path
app.config["SQLALCHEMY_DATABASE_URI"] = MYSQL_URI
app.config["SECRET_KEY"] = "sqlite3 app connection"
# Initialize the app with the extension
db.init_app(app)
with app.app_context():
    db.create_all()


migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    """Load user by its id"""
    return User.query.get(int(user_id))


class RenderError(Exception):
    """Render error for the Flask app."""

    def __init__(self, message):
        super().__init__(message)
        self.message = message


@app.route("/")
def index():
    """Index page"""
    return render_template("index.html")


@app.route("/users")
def users_all():
    """Users page"""
    users = User.query.all()
    if users is None:
        flash("No users found")
    return render_template("users_all.html", header="All Users", users=users)


@app.route("/users/add", methods=["GET", "POST"])
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


@app.route("/user/update/<int:user_id>/", methods=["GET", "POST"])
def user_update(user_id):
    """Update user"""
    user = User.query.get_or_404(user_id)
    if user is None:
        flash("User not found")
        return redirect("/users")
    form = UserForm(obj=user)
    if request.method == "POST":
        user.name = request.form.get("name").title().strip()
        user.username = request.form.get("username").title().strip()
        user.email = request.form.get("email").strip()
        db.session.commit()
        flash(f"<strong>{form.username.data}</strong> has been updated")
        return redirect("/users")
    return render_template(
        "user_update.html", header="Update User", form=form, user_id=user_id
    )


@app.route("/user/delete/<int:user_id>/", methods=["GET", "POST"])
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


@app.route("/date", methods=["GET", "POST"])
def get_date():
    """Get date"""
    return {"date": datetime.now()}


@app.errorhandler(404)
def page_not_found(_):
    """Page not found error"""
    return ("<h2>Page Not Found 404</h2>"), 404


@app.errorhandler(500)
def internarl_error(_):
    """Page not found error Internal Server Error 500"""
    return ("<h2>Internal Server Error 500</h2>"), 500


if __name__ == "__main__":
    app.run(debug=True)
