from app.extensions import db
from models.security_event import SecurityEvent


def create_security_event(
    user_id,
    event_type,
    severity,
    risk_score,
    action_taken,
    details
):
    """
    Create and store a security event.
    """

    event = SecurityEvent(
        user_id=user_id,
        event_type=event_type,
        severity=severity,
        risk_score=risk_score,
        action_taken=action_taken,
        details=details
    )

    db.session.add(event)
    db.session.commit()

    print("\n" + "=" * 60)
    print("SECURITY EVENT")
    print("=" * 60)
    print(f"Type      : {event_type}")
    print(f"Severity  : {severity}")
    print(f"Risk Score: {risk_score}")
    print(f"Action    : {action_taken}")
    print("=" * 60 + "\n")

    return event


# -------------------------------------------------------------------
# Enrollment
# -------------------------------------------------------------------

def log_enrollment_completed(user_id):
    return create_security_event(
        user_id=user_id,
        event_type="BEHAVIOR_PROFILE_ENROLLED",
        severity="LOW",
        risk_score=100,
        action_taken="Behavior profile created",
        details="User successfully completed behavioral enrollment."
    )


# -------------------------------------------------------------------
# Continuous Authentication
# -------------------------------------------------------------------

def log_continuous_auth_success(user_id, trust_score):
    return create_security_event(
        user_id=user_id,
        event_type="CONTINUOUS_AUTH_SUCCESS",
        severity="LOW",
        risk_score=trust_score,
        action_taken="No action required",
        details="Behavior successfully matched enrolled profile."
    )


def log_behavior_anomaly(user_id, trust_score):
    return create_security_event(
        user_id=user_id,
        event_type="BEHAVIOR_ANOMALY_DETECTED",
        severity="HIGH",
        risk_score=trust_score,
        action_taken="Risk engine invoked",
        details="Behavior differs from enrolled profile."
    )


# -------------------------------------------------------------------
# Step-up Authentication
# -------------------------------------------------------------------

def log_step_up_required(user_id, trust_score):
    return create_security_event(
        user_id=user_id,
        event_type="STEP_UP_AUTH_REQUIRED",
        severity="MEDIUM",
        risk_score=trust_score,
        action_taken="OTP verification required",
        details="Additional verification required before transfer."
    )


def log_otp_verified(user_id):
    return create_security_event(
        user_id=user_id,
        event_type="OTP_VERIFIED",
        severity="LOW",
        risk_score=100,
        action_taken="Identity verified",
        details="Transfer OTP verified successfully."
    )


def log_otp_failed(user_id):
    return create_security_event(
        user_id=user_id,
        event_type="OTP_FAILED",
        severity="MEDIUM",
        risk_score=0,
        action_taken="Transfer remains pending",
        details="Invalid transfer OTP entered."
    )


# -------------------------------------------------------------------
# Transfers
# -------------------------------------------------------------------

def log_transfer_completed(user_id, amount):
    return create_security_event(
        user_id=user_id,
        event_type="TRANSFER_COMPLETED",
        severity="LOW",
        risk_score=100,
        action_taken="Transfer completed",
        details=f"Transfer of ₹{amount:.2f} completed successfully."
    )


def log_transfer_blocked(user_id, trust_score):
    return create_security_event(
        user_id=user_id,
        event_type="TRANSFER_BLOCKED",
        severity="CRITICAL",
        risk_score=trust_score,
        action_taken="Transfer blocked",
        details="Transfer blocked due to behavioral risk."
    )


# -------------------------------------------------------------------
# Account Takeover
# -------------------------------------------------------------------

def log_account_takeover_detected(user_id, trust_score):
    return create_security_event(
        user_id=user_id,
        event_type="ACCOUNT_TAKEOVER_DETECTED",
        severity="CRITICAL",
        risk_score=trust_score,
        action_taken="Session should be terminated",
        details="Possible Account Takeover detected."
    )
# -------------------------------------------------------------------
# OTP Lifecycle
# -------------------------------------------------------------------

def log_otp_resent(user_id):
    return create_security_event(
        user_id=user_id,
        event_type="OTP_RESENT",
        severity="LOW",
        risk_score=100,
        action_taken="New OTP generated",
        details="User requested a new transfer OTP."
    )


def log_transfer_cancelled(user_id):
    return create_security_event(
        user_id=user_id,
        event_type="TRANSFER_CANCELLED",
        severity="LOW",
        risk_score=100,
        action_taken="Pending transfer cancelled",
        details="User cancelled the pending transfer before verification."
    )