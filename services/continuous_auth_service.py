from services.enrollment_service import enroll
from services.trust_engine import evaluate_session
from services.auth_decision_service import make_authentication_decision

from services.security_event_service import (
    log_continuous_auth_success,
    log_step_up_required,
    log_account_takeover_detected,
)

MINIMUM_KEYS = 50


def should_evaluate(session):
    """
    Evaluate every 50 keystrokes.
    """

    total_keys = len(session.typing_events)

    return (
        total_keys >= MINIMUM_KEYS
        and total_keys % MINIMUM_KEYS == 0
    )


def evaluate_if_ready(user_id, session):
    """
    Continuous behavioral authentication.
    """

    if not should_evaluate(session):
        return None

    # Enrollment
    enroll(
        user_id,
        session.id
    )

    # Trust Engine performs verification + risk evaluation
    verification = evaluate_session(
        user_id,
        session.id
    )

    if verification is None:
        return None

    # Authentication decision
    decision = make_authentication_decision(
        verification
    )

    trust_score = verification["trust_score"]
    risk_level = verification["risk_level"]

    # -------- Security Response -------- #

    if risk_level == "LOW":

        log_continuous_auth_success(
            user_id,
            trust_score
        )

    elif risk_level == "MEDIUM":

        log_step_up_required(
            user_id,
            trust_score
        )

    elif risk_level in ("HIGH", "CRITICAL"):

        log_account_takeover_detected(
            user_id,
            trust_score
        )

        # Future:
        # session.status = "TERMINATED"
        # db.session.commit()

    return {
        **verification,
        **decision
    }