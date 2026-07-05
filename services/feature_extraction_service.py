from models.typing_event import TypingEvent

from utils.statistics import (
    calculate_mean,
    calculate_variance,
    typing_speed,
)


def extract_features(events):
    """
    Extract behavioral biometric features
    from typing events.
    """

    if not events:
        return {}

    dwell_times = [
        event.dwell_time
        for event in events
    ]

    flight_times = [
        event.flight_time
        for event in events
        if event.flight_time is not None
    ]

    total_keys = len(events)

    duration = (
        events[-1].key_up_timestamp -
        events[0].key_down_timestamp
    )

    backspace_count = sum(
        1
        for event in events
        if event.key_pressed == "Backspace"
    )

    return {
        "total_keys": total_keys,
        "avg_dwell_time": calculate_mean(dwell_times),
        "avg_flight_time": calculate_mean(flight_times),
        "dwell_variance": calculate_variance(dwell_times),
        "flight_variance": calculate_variance(flight_times),
        "typing_speed": typing_speed(
            total_keys,
            duration
        ),
        "backspace_count": backspace_count,
    }


def extract_features_for_session(session_id):
    """
    Load typing events for a session
    and return extracted features.
    """

    events = (
        TypingEvent.query
        .filter_by(session_id=session_id)
        .order_by(TypingEvent.sequence_number.asc())
        .all()
    )

    return extract_features(events)