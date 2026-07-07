import random
from datetime import datetime

from app.extensions import db
from models.transfer_otp import TransferOTP

from services.security_event_service import (
    log_otp_verified,
    log_otp_failed,
    log_otp_resent,
    log_transfer_cancelled
)


def generate_transfer_otp(
    user_id,
    beneficiary,
    amount,
    note
):
    """
    Generate a new OTP for a pending transfer.
    """

    # Delete any previous unused OTP
    TransferOTP.query.filter_by(
        user_id=user_id,
        verified=False,
        is_used=False
    ).delete()

    db.session.commit()

    otp = str(random.randint(100000, 999999))

    pending = TransferOTP(
        user_id=user_id,
        otp=otp,
        beneficiary=beneficiary,
        amount=amount,
        note=note
    )

    db.session.add(pending)
    db.session.commit()

    print("\n" + "=" * 60)
    print("STEP-UP AUTHENTICATION OTP")
    print("=" * 60)
    print(f"OTP : {otp}")
    print(f"Expires : {pending.expires_at}")
    print("=" * 60 + "\n")

    return pending


def resend_transfer_otp(user_id):
    """
    Generate a fresh OTP while preserving
    the pending transfer details.
    """

    pending = (
        TransferOTP.query
        .filter_by(
            user_id=user_id,
            verified=False,
            is_used=False
        )
        .order_by(
            TransferOTP.created_at.desc()
        )
        .first()
    )

    if pending is None:
        return False, "No pending transfer found."

    beneficiary = pending.beneficiary
    amount = pending.amount
    note = pending.note

    db.session.delete(pending)
    db.session.commit()

    generate_transfer_otp(
        user_id,
        beneficiary,
        amount,
        note
    )

    log_otp_resent(user_id)

    return True, "A new OTP has been generated."


def verify_transfer_otp(
    user_id,
    entered_otp
):
    """
    Verify the submitted OTP.
    """

    pending = (
        TransferOTP.query
        .filter_by(
            user_id=user_id,
            verified=False,
            is_used=False
        )
        .order_by(
            TransferOTP.created_at.desc()
        )
        .first()
    )

    if pending is None:

        log_otp_failed(user_id)

        return False, "No pending OTP found.", None

    if datetime.utcnow() > pending.expires_at:

        db.session.delete(pending)
        db.session.commit()

        log_otp_failed(user_id)

        return False, "OTP has expired.", None

    if pending.otp != entered_otp:

        log_otp_failed(user_id)

        return False, "Invalid OTP.", None

    pending.verified = True

    db.session.commit()

    log_otp_verified(user_id)

    return True, "OTP verified successfully.", pending


def consume_verified_transfer(user_id):
    """
    Return a verified transfer and mark it used.
    """

    pending = (
        TransferOTP.query
        .filter_by(
            user_id=user_id,
            verified=True,
            is_used=False
        )
        .order_by(
            TransferOTP.created_at.desc()
        )
        .first()
    )

    if pending is None:
        return None

    pending.is_used = True

    db.session.commit()

    return pending


def cancel_pending_transfer(user_id):
    """
    Cancel any pending transfer awaiting OTP.
    """

    pending = (
        TransferOTP.query
        .filter_by(
            user_id=user_id,
            is_used=False
        )
        .all()
    )

    for otp in pending:
        db.session.delete(otp)

    db.session.commit()

    log_transfer_cancelled(user_id)

    return True