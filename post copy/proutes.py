"""post related routes"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from allwebforms import PostForm, SearchPostContent
from data_models import db, Post

# Create blueprints connection
post_bp = Blueprint("post", __name__, url_prefix="/posts", template_folder="templates")


class PostError(Exception):
    """Post error"""

    def __init__(self, message):
        self.message = message


def reset_post_form(form):
    """Reset pos form"""
    form.title.data = ""
    form.subtitle.data = ""
    form.content.data = ""


# Create search function for post content
@post_bp.route("/search", methods=["POST"])
def search():
    """Search function"""
    form = SearchPostContent()
    if form.validate_on_submit():
        searched = form.searched.data
        posts = Post.query.filter(Post.content.like("%" + searched + "%"))
        posts = posts.order_by(Post.title).all()
    return render_template("search.html", searched=searched, posts=posts)


@post_bp.route("/get_post/<int:post_id>/")
def get_post(post_id):
    """Get post"""
    post = Post.query.get_or_404(post_id)
    if post is None:
        flash("post not found")
        return redirect("/")
    return render_template("get_post.html", post=post, post_id=post_id)


@post_bp.route("/")
def posts_all():
    """posts page"""
    posts = Post.query.all()
    return render_template("posts_all.html", header="All posts", posts=posts)


@post_bp.route("/add", methods=["GET", "POST"])
@login_required
def post_add():
    """Add post"""
    if not current_user.is_authenticated:
        flash("You need to login first")
        return redirect(url_for("user.login"))
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data.title().strip(),
            subtitle=form.subtitle.data.strip(),
            content=form.content.data.strip(),
            author_id=current_user.id,
        )
        try:
            db.session.add(post)
            db.session.commit()
            flash(f"<strong>{form.title.data}</strong> has been added")
            reset_post_form(form)
        except PostError:
            flash("Operation failed during the add process")
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
        post.title = request.form.get("title").title().strip()
        post.subtitle = request.form.get("subtitle").strip()
        post.content = request.form.get("content").strip()
        try:
            db.session.commit()
            flash(f"<strong>Post ID: {post.id}</strong> has been updated")
            reset_post_form(form)
        except PostError:
            flash("Operation failed during the update process")
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
    flash(f"<strong>Post ID: {post.id}</strong> has been deleted")
    try:
        db.session.delete(post)
        db.session.commit()
    except PostError:
        flash("Operation failed during the delete process")
    return redirect("/posts")
