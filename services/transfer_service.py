from app.extensions import db

from models.bank_account import BankAccount
from models.transaction import Transaction
from models.user_session import UserSession

from services.verification_service import verify
from services.transaction_risk_service import (
    evaluate_transaction_risk
)

from services.otp_service import (
    generate_transfer_otp
)

from services.security_event_service import (
    log_step_up_required,
    log_account_takeover_detected,
    log_transfer_blocked,
    log_transfer_completed,
    log_behavior_anomaly
)

from services.session_service import (
    terminate_active_session
)


def execute_transfer(user, beneficiary, amount, note):
    """
    Execute a verified money transfer.
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

    # -----------------------------------------
    # Security Audit
    # -----------------------------------------

    log_transfer_completed(
        user.id,
        amount
    )

    print("\n" + "=" * 60)
    print("TRANSFER SUCCESSFUL")
    print("=" * 60)

    return True, "Transfer completed successfully."


_DECISION_LABELS = {
    "LOW": "TRANSFER ALLOWED",
    "MEDIUM": "MONITOR",
    "HIGH": "OTP REQUIRED",
    "CRITICAL": "TRANSFER BLOCKED",
}


def _print_fraud_analysis(risk):
    """
    Prints the transaction fraud analysis breakdown returned by
    transaction_risk_service.evaluate_transaction_risk().
    """

    print("\n" + "=" * 60)
    print("TRANSACTION FRAUD ANALYSIS")
    print("=" * 60)
    print(f"Behavior Score    : {risk.get('behavior_score')}")
    print(f"Amount Score      : {risk.get('amount_score')}")
    print(f"Balance Score     : {risk.get('balance_score')}")
    print(f"Beneficiary Score : {risk.get('beneficiary_score')}")
    print(f"Velocity Score    : {risk.get('velocity_score')}")
    print("\n" + "-" * 60)
    print(f"Overall Score     : {risk.get('overall_score')}")
    print(f"Risk Level        : {risk.get('risk_level')}")

    if risk["reasons"]:
        print("\nReasons")

        for reason in risk["reasons"]:
            print(f"- {reason}")

    print("\n" + "=" * 60)


def transfer_money(user, beneficiary, amount, note):
    """
    Secure transfer protected by behavioral biometrics.
    """

    session = (
        UserSession.query
        .filter_by(
            user_id=user.id,
            status="ACTIVE"
        )
        .order_by(UserSession.login_time.desc())
        .first()
    )

    if session:

        verification = verify(
            user.id,
            session.id
        )

        print("\n" + "=" * 60)
        print("TRANSFER VERIFICATION")
        print("=" * 60)
        print(verification)

        if verification:

            trust_score = verification["trust_score"]

            risk = evaluate_transaction_risk(
                user=user,
                beneficiary=beneficiary,
                amount=amount,
                trust_score=trust_score
            )

            _print_fraud_analysis(risk)

            print(f"Decision : {_DECISION_LABELS.get(risk['risk_level'], 'UNKNOWN')}")

            # Record anomaly whenever
            # trust drops below LOW.

            if risk["risk_level"] in [
                "MEDIUM",
                "HIGH",
                "CRITICAL"
            ]:
                log_behavior_anomaly(
                    user.id,
                    risk["overall_score"]
                )

            # -----------------------------------------
            # LOW
            # -----------------------------------------

            if risk["risk_level"] == "LOW":

                return execute_transfer(
                    user,
                    beneficiary,
                    amount,
                    note
                )

            # -----------------------------------------
            # MEDIUM
            # -----------------------------------------

            elif risk["risk_level"] == "MEDIUM":

                print("MEDIUM RISK - Monitoring")

                return execute_transfer(
                    user,
                    beneficiary,
                    amount,
                    note
                )

            # -----------------------------------------
            # HIGH
            # -----------------------------------------

            elif risk["risk_level"] == "HIGH":

                generate_transfer_otp(
                    user.id,
                    beneficiary,
                    amount,
                    note
                )

                log_step_up_required(
                    user.id,
                    risk["overall_score"]
                )

                print("HIGH RISK - OTP GENERATED")

                return (
                    False,
                    "OTP_REQUIRED"
                )

            # -----------------------------------------
            # CRITICAL
            # -----------------------------------------

            elif risk["risk_level"] == "CRITICAL":

                log_account_takeover_detected(
                    user.id,
                    risk["overall_score"]
                )

                log_transfer_blocked(
                    user.id,
                    risk["overall_score"]
                )

                terminate_active_session(
                    user.id
                )

                print("CRITICAL RISK - SESSION TERMINATED")

                return (
                    False,
                    "SESSION_TERMINATED"
                )

    return execute_transfer(
        user,
        beneficiary,
        amount,
        note
    )
