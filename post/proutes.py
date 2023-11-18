"""post related routes"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from allwebforms import PostForm
from data_models import db, Post

# Create blueprints connection
post_bp = Blueprint("post", __name__, url_prefix="/posts", template_folder="templates")


def reset_post_form(form):
    """Reset pos form"""
    form.title.data = ""
    form.subtitle.data = ""
    form.content.data = ""


@post_bp.route("/")
def posts_all():
    """posts page"""
    posts = Post.query.all()
    return render_template("posts_all.html", header="All posts", posts=posts)


@post_bp.route("/add", methods=["GET", "POST"])
@login_required
def post_add():
    """Add pos"""
    if not current_user.is_authenticated:
        flash("You need to login first")
        return redirect("/users/login")
        # return redirect(url_for("user.login"))

    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data.title().strip(),
            subtitle=form.subtitle.data.strip(),
            content=form.content.data.strip(),
            author_id=current_user.id,
        )
        db.session.add(post)
        db.session.commit()
        flash(f"<strong>{form.title.data}</strong> has been added")
        reset_post_form(form)
        return redirect("/posts")
    return render_template("post_add.html", header="Add Post", form=form)


@post_bp.route("/post/update/<int:post_id>/", methods=["GET", "POST"])
@login_required
def post_update(post_id):
    """Update post"""
    post = Post.query.get_or_404(post_id)
    if not current_user.id == post.author_id:
        flash("You can only update your own post")
        return redirect("/posts")
    if post is None:
        flash("post not found")
        return redirect("/posts/all")
    form = PostForm(obj=post)
    if request.method == "POST":
        post.name = request.form.get("name").title().strip()
        post.postname = request.form.get("postname").strip()
        post.email = request.form.get("email").strip()
        db.session.commit()
        flash(f"<strong>{form.postname.data}</strong> has been updated")
        reset_post_form(form)
        return redirect(url_for("post.posts_all"))
    return render_template(
        "post_update.html", header="Update post", form=form, post_id=post_id
    )


@post_bp.route("/post/delete/<int:post_id>/", methods=["GET", "POST"])
@login_required
def post_delete(post_id):
    """Delete post"""
    post = Post.query.get_or_404(post_id)
    if not current_user.id == post.author_id:
        flash("You can only delete your own post")
        return redirect("/posts")
    if post is None:
        flash("post not found")
        return redirect("/posts")
    db.session.delete(post)
    db.session.commit()
    flash(f"<strong>{post.postname}</strong> has been deleted")
    return redirect("/posts")
