from app.shared.extensions import db
from datetime import datetime


class Translation(db.Model):
    __tablename__ = "translations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True)
    password_hash = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)

    translations = db.relationship(
        "Translation", backref="user", cascade="all, delete-orphan"
    )
