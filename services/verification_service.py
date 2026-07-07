from services.feature_extraction_service import extract_features_for_session
from services.profile_service import get_behavior_profile
from services.similarity_service import calculate_similarity
from services.trust_score_service import calculate_trust_score


def verify(user_id, session_id):
    """
    Verify the current typing session against the
    enrolled behavioral profile.
    """

    profile = get_behavior_profile(user_id)

    if profile is None:
        return None

    if not profile.is_enrolled:
        return None

    current_features = extract_features_for_session(
        session_id
    )

    if current_features is None:
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

        "keys_collected": current_features["total_keys"]

    }