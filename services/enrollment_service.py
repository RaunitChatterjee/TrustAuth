from datetime import datetime

from app.extensions import db

from models.behavior_profile import BehaviorProfile
from services.feature_extraction_service import extract_features_for_session

MINIMUM_ENROLLMENT_KEYS = 100


def enroll(user_id, session_id):
    """
    Create the user's baseline typing profile.
    Runs only once.
    """

    features = extract_features_for_session(session_id)

    if not features:
        return None

    if features["total_keys"] < MINIMUM_ENROLLMENT_KEYS:
        return None

    profile = BehaviorProfile.query.filter_by(
        user_id=user_id
    ).first()

    if profile:

        return profile

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