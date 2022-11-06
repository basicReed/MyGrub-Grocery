"""SQLAlchemy models for MyGrub"""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class Favorites(db.Model):
    __tablename__ = 'favorites'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"), primary_key=True)
    recipe_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.Text,
        nullable=False,
    )
    img_url = db.Column(db.Text)


class Groceries(db.Model):
    __tablename__ = 'groceries'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"), primary_key=True)
    ingredient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.Text,
        nullable=False,
    )



class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )   

    groceries = db.relationship(
        "User",
        secondary="groceries",
        primaryjoin=(Groceries.user_id == id)
        # secondaryjoin=(Follows.user_following_id == id)
    ) 

    favorites = db.relationship(
        "User",
        secondary="favorites",
        primaryjoin=(Favorites.user_id == id)
        # secondaryjoin=(Favorites.user_being_followed_id == id)
    ) 


    # grocery = db.relationship('Groceries', back_populates = "users")

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)