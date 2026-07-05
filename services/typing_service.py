from app.extensions import db

from models.typing_event import TypingEvent
from services.session_service import (
    get_active_session,
    update_last_activity,
)


def save_typing_event(user, data):
    """
    Save a single typing event for the user's
    active session.
    """

    session = get_active_session(user.id)

    if not session:
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

    return True, event