from services.feature_extraction_service import extract_features_for_session
from services.profile_service import (
    get_behavior_profile,
    enroll_user,
    MINIMUM_ENROLLMENT_KEYS
)
from services.similarity_service import calculate_similarity
from services.trust_score_service import calculate_trust_score


def evaluate_session(user_id, session_id):
    """
    TrustAuth Evaluation Engine

    Phase 1:
        Enrollment

    Phase 2:
        Continuous Verification
    """

    profile = get_behavior_profile(user_id)

    # User not enrolled yet
    if profile is None or not profile.is_enrolled:

        enrolled_profile = enroll_user(
            user_id,
            session_id
        )

        current_features = extract_features_for_session(
            session_id
        )

        total_keys = 0

        if current_features:
            total_keys = current_features["total_keys"]

        # Still collecting baseline
        if enrolled_profile is None:

            return {
                "enrolled": False,
                "similarity": None,
                "trust_score": None,
                "risk_level": "ENROLLING",
                "keys_collected": total_keys,
                "keys_required": MINIMUM_ENROLLMENT_KEYS
            }

        # Enrollment completed
        profile = enrolled_profile

    current_features = extract_features_for_session(
        session_id
    )

    if not current_features:
        return None

    similarity = calculate_similarity(
        profile,
        current_features
    )

    trust = calculate_trust_score(
        similarity
    )

    return {
        "enrolled": True,
        "similarity": similarity,
        "trust_score": trust["trust_score"],
        "risk_level": trust["risk_level"],
        "keys_collected": current_features["total_keys"],
        "keys_required": MINIMUM_ENROLLMENT_KEYS
    }