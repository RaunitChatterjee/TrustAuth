from datetime import datetime

from app.extensions import db
from models.behavior_profile import BehaviorProfile

from services.feature_extraction_service import (
    extract_features_for_session
)

from services.security_event_service import (
    log_enrollment_completed
)

# Development threshold.
# Change back to 100 before the final project submission.
MINIMUM_ENROLLMENT_KEYS = 20


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
    Create the user's behavioral profile once enough
    keystrokes have been collected.
    """

    profile = get_behavior_profile(user_id)

    # Already enrolled
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

    # -----------------------------------------
    # Security Audit Log
    # -----------------------------------------

    log_enrollment_completed(user_id)

    print("\n" + "=" * 60)
    print("USER ENROLLED")
    print("=" * 60)
    print(f"User ID: {user_id}")
    print(f"Keystrokes: {features['total_keys']}")
    print("=" * 60 + "\n")

    return profile