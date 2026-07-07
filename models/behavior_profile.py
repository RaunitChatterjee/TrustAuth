from datetime import datetime

from app.extensions import db


class BehaviorProfile(db.Model):
    __tablename__ = "behavior_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    # Enrollment Status
    is_enrolled = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    enrollment_completed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    # Behavioral Features
    avg_dwell_time = db.Column(db.Float, nullable=False)
    avg_flight_time = db.Column(db.Float, nullable=False)

    dwell_variance = db.Column(db.Float, nullable=False)
    flight_variance = db.Column(db.Float, nullable=False)

    typing_speed = db.Column(db.Float, nullable=False)

    total_keys = db.Column(db.Integer, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<BehaviorProfile User {self.user_id}>"