from app.extensions import db

from models.typing_event import TypingEvent

from services.session_service import (
    get_active_session,
    update_last_activity,
)

from services.continuous_auth_service import evaluate_if_ready


def save_typing_event(user, data):
    """
    Save a typing event and trigger
    continuous behavioral authentication.
    """

    session = get_active_session(user.id)

    if session is None:
        return False, "No active session found."

    event = TypingEvent(
        session_id=session.id,
        field_name=data["field_name"],
        key_pressed=data["key_pressed"],
        sequence_number=data["sequence_number"],
        key_down_timestamp=data["key_down_timestamp"],
        key_up_timestamp=data["key_up_timestamp"],
        dwell_time=data["dwell_time"],
        flight_time=data.get("flight_time")
    )

    db.session.add(event)

    update_last_activity(session)

    db.session.commit()

    authentication = evaluate_if_ready(
        user.id,
        session
    )

    response = {
        "event": event,
        "authentication": authentication
    }

    return True, response