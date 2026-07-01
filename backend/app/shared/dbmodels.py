from app.shared.extensions import db
from datetime import datetime


class Translation(db.Model):
    """
    Database model representing a saved word translation record.
    """

    __tablename__ = "translations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    """A unique ID for the translation record."""
    word = db.Column(db.Text, nullable=False)
    """The word that was translated."""
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    """The date and time when the request was created."""
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    """The owner-user unique ID"""


class User(db.Model):
    """
    Database model representing an application user.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    """A unique ID for the user."""
    name = db.Column(db.Text, unique=True)
    """The unique name of the user."""
    password_hash = db.Column(db.Text)
    """The password hash string."""
    is_admin = db.Column(db.Boolean, default=False)
    """Indicates whether the user has administrator privileges."""

    translations = db.relationship(
        "Translation", backref="user", cascade="all, delete-orphan"
    )
