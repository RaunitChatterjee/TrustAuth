from datetime import datetime, timedelta

from app.extensions import db


class TransferOTP(db.Model):
    __tablename__ = "transfer_otps"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    otp = db.Column(
        db.String(6),
        nullable=False
    )

    beneficiary = db.Column(
        db.String(100),
        nullable=False
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    note = db.Column(
        db.String(255)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    expires_at = db.Column(
        db.DateTime,
        default=lambda: datetime.utcnow() + timedelta(minutes=5)
    )

    verified = db.Column(
        db.Boolean,
        default=False
    )

    is_used = db.Column(
        db.Boolean,
        default=False
    )