from datetime import datetime, timedelta

from models.bank_account import BankAccount
from models.transaction import Transaction


def calculate_behavior_risk(trust_score):
    """
    Convert trust score to risk points.
    Higher points = higher risk.
    """

    if trust_score is None:
        return 100

    return max(0, int(100 - trust_score))


def calculate_amount_risk(amount):

    if amount < 5000:
        return 0

    elif amount < 20000:
        return 10

    elif amount < 50000:
        return 20

    elif amount < 100000:
        return 30

    return 40


def calculate_balance_risk(user, amount):
    """
    Risk based on percentage of account balance.
    """

    account = BankAccount.query.filter_by(
        user_id=user.id
    ).first()

    if not account:
        return 0

    percent = (amount / account.balance) * 100

    if percent < 10:
        return 0

    elif percent < 25:
        return 10

    elif percent < 50:
        return 20

    return 35


def calculate_beneficiary_risk(user, beneficiary):

    account = BankAccount.query.filter_by(
        user_id=user.id
    ).first()

    if not account:
        return 0

    previous = Transaction.query.filter_by(
        account_id=account.id,
        recipient=beneficiary
    ).count()

    if previous == 0:
        return 15

    return 0


def calculate_velocity_risk(user):

    account = BankAccount.query.filter_by(
        user_id=user.id
    ).first()

    if not account:
        return 0

    five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)

    transfers = Transaction.query.filter(
        Transaction.account_id == account.id,
        Transaction.created_at >= five_minutes_ago
    ).count()

    if transfers >= 5:
        return 20

    elif transfers >= 3:
        return 10

    return 0


def overall_risk_level(score):

    if score < 40:
        return "LOW"

    elif score < 70:
        return "MEDIUM"

    elif score < 100:
        return "HIGH"

    return "CRITICAL"


def evaluate_transaction_risk(
    user,
    beneficiary,
    amount,
    trust_score
):

    behavior = calculate_behavior_risk(
        trust_score
    )

    amount_risk = calculate_amount_risk(
        amount
    )

    balance_risk = calculate_balance_risk(
        user,
        amount
    )

    beneficiary_risk = calculate_beneficiary_risk(
        user,
        beneficiary
    )

    velocity_risk = calculate_velocity_risk(
        user
    )

    overall = (
        behavior +
        amount_risk +
        balance_risk +
        beneficiary_risk +
        velocity_risk
    )

    reasons = []

    if behavior > 30:
        reasons.append("Behavior anomaly")

    if amount_risk:
        reasons.append("High transaction amount")

    if balance_risk:
        reasons.append("Large percentage of account balance")

    if beneficiary_risk:
        reasons.append("New beneficiary")

    if velocity_risk:
        reasons.append("Rapid transaction activity")

    return {

        "behavior_score": behavior,

        "amount_score": amount_risk,

        "balance_score": balance_risk,

        "beneficiary_score": beneficiary_risk,

        "velocity_score": velocity_risk,

        "overall_score": overall,

        "risk_level": overall_risk_level(overall),

        "reasons": reasons

    }