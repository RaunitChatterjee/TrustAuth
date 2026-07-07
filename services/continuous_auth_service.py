from services.enrollment_service import enroll
from services.verification_service import verify
from services.risk_engine import evaluate_risk
from services.auth_decision_service import make_authentication_decision
from services.security_event_service import create_security_event

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
    Continuous behavioral authentication pipeline.
    """

    if not should_evaluate(session):
        return None

    # Step 1: Ensure enrollment exists
    enroll(user_id, session.id)

    # Step 2: Verify current behavior
    verification = verify(
        user_id,
        session.id
    )

    # User still enrolling
    if verification is None:
        return None

    # Step 3: Calculate banking risk
    risk = evaluate_risk(
        verification["trust_score"]
    )

    # Step 4: Authentication decision
    decision = make_authentication_decision(
        risk
    )

    # Step 5: Security Event
    create_security_event(
        user_id=user_id,
        event_type="CONTINUOUS_AUTH",
        severity=risk["risk_level"],
        risk_score=verification["trust_score"],
        action_taken=decision["decision"],
        details=decision["message"]
    )

    return {
        **verification,
        **risk,
        **decision
    }