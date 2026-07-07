from models.behavior_profile import BehaviorProfile


def get_behavior_profile(user_id):
    """
    Return the enrolled behavioral profile
    for a user.
    """

    return BehaviorProfile.query.filter_by(
        user_id=user_id
    ).first()


def is_user_enrolled(user_id):
    """
    Check whether the user has completed
    behavioral enrollment.
    """

    profile = get_behavior_profile(user_id)

    if profile is None:
        return False

    return profile.is_enrolled