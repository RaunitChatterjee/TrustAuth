from datetime import datetime

from app.extensions import db


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    account_id = db.Column(
        db.Integer,
        db.ForeignKey("bank_accounts.id"),
        nullable=False
    )

    transaction_type = db.Column(
        db.String(20),
        nullable=False
    )

    recipient = db.Column(
        db.String(120),
        nullable=False
    )

    note = db.Column(
        db.String(255)
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Completed"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    account = db.relationship(
        "BankAccount",
        backref=db.backref(
            "transactions",
            lazy=True,
            cascade="all, delete-orphan"
        )
    )

    def __repr__(self):
        return (
            f"<Transaction {self.id} | "
            f"{self.transaction_type} | "
            f"{self.amount}>"
        )