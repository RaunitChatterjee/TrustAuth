from app.extensions import db


class TypingEvent(db.Model):
    __tablename__ = "typing_events"

    id = db.Column(db.Integer, primary_key=True)

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
        db.String(10),
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
        db.Float,
        nullable=True
    )

    session = db.relationship(
        "UserSession",
        back_populates="typing_events"
    )

    def __repr__(self):
        return f"<TypingEvent {self.key_pressed}>"