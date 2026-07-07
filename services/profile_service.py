from datetime import datetime

from app.extensions import db
from models.behavior_profile import BehaviorProfile
from services.feature_extraction_service import extract_features_for_session

MINIMUM_ENROLLMENT_KEYS = 100


def get_behavior_profile(user_id):
    """
    Return the behavioral profile for a user.
    """

    return BehaviorProfile.query.filter_by(
        user_id=user_id
    ).first()


def is_user_enrolled(user_id):
    """
    Check whether the user has completed enrollment.
    """

    profile = get_behavior_profile(user_id)

    if profile is None:
        return False

    return profile.is_enrolled


def enroll_user(user_id, session_id):
    """
    Compatibility function.

    This keeps the existing routes.py and trust_engine.py
    working while we finish integrating the backend.
    """

    profile = get_behavior_profile(user_id)

    if profile:
        return profile

    features = extract_features_for_session(session_id)

    if not features:
        return None

    if features["total_keys"] < MINIMUM_ENROLLMENT_KEYS:
        return None

    profile = BehaviorProfile(
        user_id=user_id,
        is_enrolled=True,
        enrollment_completed_at=datetime.utcnow(),
        avg_dwell_time=features["avg_dwell_time"],
        avg_flight_time=features["avg_flight_time"],
        dwell_variance=features["dwell_variance"],
        flight_variance=features["flight_variance"],
        typing_speed=features["typing_speed"],
        total_keys=features["total_keys"]
    )

    db.session.add(profile)
    db.session.commit()

    return profile