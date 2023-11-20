"""book related routes"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import asc, desc, func
from allwebforms import BookForm, SearchForm
from data_models import db, Book, Author
from book_api import get_book_cover_url

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
    form.isbn.data = ""
    form.publication_year.data = ""
    form.condition.data = ""


@book_bp.route("/search", methods=["POST"])
def search():
    """Search book by title or author by name"""
    form = SearchForm(request.form)
    if form.validate_on_submit():
        searched = form.searched.data.lower().strip()
        print(f"Search Text: {searched}")

        books = Book.query.filter(func.lower(Book.title).like(f"%{searched}%")).all()
        print("Books:")
        for book in books:
            print(book.title)

        authors = Author.query.filter(
            func.lower(Author.name).like(f"%{searched}%")
        ).all()
        print("Authors:")
        for author in authors:
            print(author.name)

    return render_template(
        "search.html", searched=searched, books=books, authors=authors
    )


@book_bp.route("/get_book/<int:book_id>/")
def get_book(book_id):
    """Get book"""
    book = Book.query.get_or_404(book_id)
    if book is None:
        flash("book not found")
        return redirect("/")
    return render_template("get_book.html", book=book, book_id=book_id)


@book_bp.route("/", methods=["GET"])
def books_all():
    """Books page"""
    valid_sort_params = ["title", "author"]
    sort_param = request.args.get("sort")
    if sort_param in valid_sort_params:
        order_param = request.args.get("order", "asc")
        order_function = asc if order_param == "asc" else desc
        if sort_param == "author":
            # Bellow methods sometimes does not give the expected result
            # books = Book.query.order_by(order_function(Book.author_id.name)).all()
            books = (
                Book.query.join(Author)
                .order_by(order_function(getattr(Author, "name")))
                .all()
            )
        else:
            books = Book.query.order_by(order_function(getattr(Book, sort_param))).all()
    else:
        books = Book.query.all()
    return render_template("books_all.html", header="All Books", books=books)


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
        # query to checj author if exists
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
            isbn=form.isbn.data.strip(),
            publication_year=form.publication_year.data,
            cover_url=get_book_cover_url(form.isbn.data.strip()),
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
        book.publication_year = request.form.get("publication_year")
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
