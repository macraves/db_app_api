"""book related routes"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from allwebforms import BookForm, AuthorForm
from data_models import db, Book, Author

# Create blueprints connection
book_bp = Blueprint("book", __name__, url_prefix="/books", template_folder="templates")


class BookError(Exception):
    """book error"""

    def __init__(self, message):
        self.message = message


def reset_book_form(form):
    """Reset pos form"""
    form.title.data = ""
    form.author.data = ""
    form.condition.data = ""


@book_bp.route("/get_book/<int:book_id>/")
def get_book(book_id):
    """Get book"""
    book = Book.query.get_or_404(book_id)
    if book is None:
        flash("book not found")
        return redirect("/")
    return render_template("get_book.html", book=book, book_id=book_id)


@book_bp.route("/")
def books_all():
    """books page"""
    books = Book.query.all()
    return render_template("books_all.html", header="All books", books=books)


@book_bp.route("/add", methods=["GET", "POST"])
@login_required
def book_add():
    """Add book"""
    if not current_user.is_authenticated:
        flash("You need to login first")
        return redirect(url_for("user.login"))
    form = BookForm()
    if form.validate_on_submit():
        author_name = form.author.data.title().strip()
        # Check if the author already exists
        author = Author.query.filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)
            db.session.add(author)
            db.session.commit()
        book = Book(
            title=form.title.data.title().strip(),
            condition=form.condition.data.lower().strip(),
            author=author,
            user_id=current_user.id,
        )
        try:
            db.session.add(book)
            db.session.commit()
            flash(f"<strong>{form.title.data}</strong> has been added")
            reset_book_form(form)
        except BookError:
            flash("Operation failed during the add process")
        return redirect("/books")
    return render_template("book_add.html", header="Add book", form=form)


@book_bp.route("/book/update/<int:book_id>/", methods=["GET", "POST"])
@login_required
def book_update(book_id):
    """Update book"""
    book = Book.query.get_or_404(book_id)
    if book is None:
        flash("book not found")
        return redirect("/books/all")
    form = BookForm(obj=book)
    if request.method == "POST":
        book.title = request.form.get("title").title().strip()
        book.condition = request.form.get("condition").lower().strip()
        try:
            db.session.commit()
            flash(f"<strong>book ID: {book.id}</strong> has been updated")
            reset_book_form(form)
        except BookError:
            flash("Operation failed during the update process")
        return redirect(url_for("book.books_all"))
    return render_template(
        "book_update.html", header="Update book", form=form, book_id=book_id
    )


@book_bp.route("/book/delete/<int:book_id>/", methods=["GET", "POST"])
@login_required
def book_delete(book_id):
    """Delete book"""
    book = Book.query.get_or_404(book_id)
    if book is None:
        flash("book not found")
        return redirect("/books")
    flash(f"<strong>book ID: {book.id}</strong> has been deleted")
    try:
        db.session.delete(book)
        db.session.commit()
    except BookError:
        flash("Operation failed during the delete process")
    return redirect("/books")
