"""MySQL and SQLite data models for Book Alchemy.
ORM objects methods and rules for the database."""

import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


script_root = os.path.dirname(os.path.realpath(__file__))
data_folder_root = os.path.join(script_root, "data")
if not os.path.exists(data_folder_root):
    os.makedirs(data_folder_root)
    print(f"Created {data_folder_root}")


MYSQL_URI = f"sqlite:///{data_folder_root}/library.sqlite"

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """user has uniqe id and can have many books and posts"""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    about_user = db.Column(db.String(100), nullable=True)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))
    books = db.relationship("Book", backref="user", lazy=True)
    posts = db.relationship("Post", backref="user", lazy=True)

    @property
    def password(self):
        """Password property getter method
        Calling Users.password raises this Error."""
        raise AttributeError("password is not a readable attribute!!!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Verify password for the user."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"Name: '{self.name}', Email: '{self.email}', Added: '{self.added_date}'"


class Author(db.Model):
    """author can write many books"""

    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.DateTime, default=datetime.utcnow)
    death_date = db.Column(db.DateTime, default=datetime.utcnow)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)
    books = db.relationship("Book", backref="author", lazy=True)


class Book(db.Model):
    """book has only one author as its author_id,
    same book can be added by many users"""

    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    title = db.Column(db.String(100), nullable=False)
    condition = db.Column(db.String(100), nullable=False)
    added_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Book('{self.title}', '{self.author}', '{self.added_date}')"


# Create a Blog Post Model
class Post(db.Model):
    """post can be added only one user"""

    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    # Large text
    content = db.Column(db.Text, nullable=False)

    def __repr__(self) -> str:
        return f"Blog Post('{self.title}', '{self.subtitle}', '{self.date_posted}')"
