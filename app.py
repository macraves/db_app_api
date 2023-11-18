"""Flask app for database, create its database extension, and create its table."""
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_login import LoginManager
from data_models import datetime, db, MYSQL_URI, User
from user.uroutes import user_bp
from post.proutes import post_bp

app = Flask(__name__)
# Create sqlite3 library.db by defined file path
app.config["SQLALCHEMY_DATABASE_URI"] = MYSQL_URI
app.config["SECRET_KEY"] = "sqlite3 app connection"
# Initialize the app with the extension
db.init_app(app)
with app.app_context():
    db.create_all()


migrate = Migrate(app, db)
# Registry for blueprints
app.register_blueprint(user_bp, url_prefix="/users")
app.register_blueprint(post_bp, url_prefix="/posts")


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
