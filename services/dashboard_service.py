from models.bank_account import BankAccount
from models.transaction import Transaction


def get_dashboard_data(user):
    """
    Returns all dashboard data for the logged-in user.
    """

    account = BankAccount.query.filter_by(
        user_id=user.id
    ).first()

    recent_transactions = []

    if account:
        recent_transactions = (
            Transaction.query
            .filter_by(account_id=account.id)
            .order_by(Transaction.created_at.desc())
            .limit(5)
            .all()
        )

    return {
        "account": account,
        "transactions": recent_transactions
    }