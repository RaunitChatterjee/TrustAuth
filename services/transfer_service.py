from app.extensions import db
from models.bank_account import BankAccount
from models.transaction import Transaction


def transfer_money(user, beneficiary, amount, note):
    """
    Process a money transfer.
    """

    account = BankAccount.query.filter_by(
        user_id=user.id
    ).first()

    if not account:
        return False, "Bank account not found."

    if amount <= 0:
        return False, "Amount must be greater than zero."

    if account.balance < amount:
        return False, "Insufficient balance."

    account.balance -= amount

    transaction = Transaction(
        account_id=account.id,
        transaction_type="Debit",
        recipient=beneficiary,
        amount=amount,
        note=note,
        status="Completed"
    )

    db.session.add(transaction)
    db.session.commit()

    return True, "Transfer completed successfully."