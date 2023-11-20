"""Author related routes"""
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from allwebforms import AuthorForm
from data_models import db, Author, Book

# Create blueprints connection
author_bp = Blueprint(
    "author", __name__, url_prefix="/authors", template_folder="templates"
)


class AuthorError(Exception):
    """Author error"""

    def __init__(self, message):
        self.message = message


def reset_author_form(form):
    """Reset pos form"""
    form.name.data = ""
    form.birth_date.data = ""
    form.death_date.data = ""


@author_bp.route("/get_author/<int:author_id>/")
def get_author(author_id):
    """Get author by id"""
    author = Author.query.get_or_404(author_id)
    return render_template("get_author.html", author=author, author_id=author_id)


# Adding a new author
@author_bp.route("/add", methods=["GET", "POST"])
@login_required
def author_add():
    """Add author"""
    if not current_user.is_authenticated:
        flash("You need to login first")
        return redirect(url_for("user.login"))
    form = AuthorForm()
    if form.validate_on_submit():
        author_name = form.name.data.title().strip()
        # Check if the author already exists
        author = Author.query.filter_by(name=author_name).first()
        if not author:
            author = Author(
                name=author_name,
                birth_date=form.birth_date.data,
                death_date=form.death_date.data,
            )
            db.session.add(author)
            db.session.commit()
        flash(f"<strong>{form.name.data}</strong> has been added")
        reset_author_form(form)
        return redirect("/")
    else:
        # Display form errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    f"Error in field '{getattr(form, field).label.text}': {error}",
                    "error",
                )
    return render_template("author_add.html", header="Add author", form=form)


# Updating an author
@author_bp.route("/update/<int:author_id>/", methods=["GET", "POST"])
@login_required
def author_update(author_id):
    """Update author"""
    author = Author.query.get_or_404(author_id)
    if author is None:
        flash("Author not found")
        return redirect("/")
    form = AuthorForm(obj=author)
    if form.validate_on_submit():
        form.populate_obj(author)
        try:
            db.session.commit()
            flash(f"Author ID: {author.id} has been updated")
            return redirect(url_for("author.authors_all"))
        except AuthorError:
            flash("Operation failed during the update process")
    else:
        # Display form errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    f"Error in field '{getattr(form, field).label.text}': {error}",
                    "error",
                )
    return render_template(
        "author_update.html", header="Update author", form=form, author_id=author_id
    )


# Author list
@author_bp.route("/")
def authors_all():
    """authors page"""
    authors = Author.query.all()
    return render_template("authors_all.html", header="All authors", authors=authors)


# Delete author
@author_bp.route("/delete/<int:author_id>/", methods=["GET", "POST"])
@login_required
def author_delete(author_id):
    """Delete author, Only authorized user can delete author"""
    if current_user.id == 1:
        author = Author.query.get_or_404(author_id)
        if author is None:
            flash("author not found")
            return redirect("/")

        # First book needs to be deleted
        books_to_delete = Book.query.filter_by(author_id=author.id).all()
        for book in books_to_delete:
            db.session.delete(book)
        flash(
            f"<strong>author ID: {author.id}</strong> and associated books have been deleted"
        )
        # then author
        try:
            db.session.delete(author)
            db.session.commit()
        except AuthorError:
            flash("Operation failed during the delete author")
    return redirect("/")
