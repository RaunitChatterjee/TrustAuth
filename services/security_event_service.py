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
    Create a security event.
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

    return event