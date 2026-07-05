from datetime import datetime

from app.extensions import db


class TypingEvent(db.Model):
    __tablename__ = "typing_events"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    session_id = db.Column(
        db.Integer,
        db.ForeignKey("sessions.id"),
        nullable=False
    )

    field_name = db.Column(
        db.String(50),
        nullable=False
    )

    key_pressed = db.Column(
        db.String(20),
        nullable=False
    )

    sequence_number = db.Column(
        db.Integer,
        nullable=False
    )

    key_down_timestamp = db.Column(
        db.Float,
        nullable=False
    )

    key_up_timestamp = db.Column(
        db.Float,
        nullable=False
    )

    dwell_time = db.Column(
        db.Float,
        nullable=False
    )

    flight_time = db.Column(
        db.Float
    )

    captured_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    session = db.relationship(
        "UserSession",
        back_populates="typing_events"
    )

    def __repr__(self):
        return (
            f"<TypingEvent "
            f"Session={self.session_id} "
            f"Field={self.field_name} "
            f"Key={self.key_pressed}>"
        )