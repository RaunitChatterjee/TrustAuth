from datetime import datetime

from app.extensions import db


class SecurityEvent(db.Model):
    __tablename__ = "security_events"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    event_type = db.Column(
        db.String(50),
        nullable=False
    )

    severity = db.Column(
        db.String(20),
        nullable=False
    )

    risk_score = db.Column(
        db.Float,
        nullable=False
    )

    action_taken = db.Column(
        db.String(100),
        nullable=False
    )

    details = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        back_populates="security_events"
    )

    def __repr__(self):
        return f"<SecurityEvent {self.event_type}>"