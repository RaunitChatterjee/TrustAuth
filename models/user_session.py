from datetime import datetime

from app.extensions import db


class UserSession(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    login_time = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    last_activity = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    logout_time = db.Column(
        db.DateTime
    )

    ip_address = db.Column(
        db.String(45)
    )

    device_info = db.Column(
        db.String(120)
    )

    status = db.Column(
        db.String(20),
        default="ACTIVE"
    )

    user = db.relationship(
        "User",
        back_populates="sessions"
    )

    typing_events = db.relationship(
        "TypingEvent",
        back_populates="session",
        cascade="all, delete-orphan"
    )