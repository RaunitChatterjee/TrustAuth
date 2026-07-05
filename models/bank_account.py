from datetime import datetime

from app.extensions import db


class BankAccount(db.Model):
    __tablename__ = "bank_accounts"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    account_number = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    account_type = db.Column(
        db.String(20),
        default="Savings"
    )

    balance = db.Column(
        db.Float,
        default=100000.00
    )

    currency = db.Column(
        db.String(10),
        default="INR"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref=db.backref(
            "bank_account",
            uselist=False
        )
    )

    def __repr__(self):
        return f"<BankAccount {self.account_number}>"