def calculate_similarity(profile, current_features):
    """
    Calculate normalized similarity between the
    enrolled profile and the current typing session.
    """

    features = [

        (
            profile.avg_dwell_time,
            current_features["avg_dwell_time"]
        ),

        (
            profile.avg_flight_time,
            current_features["avg_flight_time"]
        ),

        (
            profile.dwell_variance,
            current_features["dwell_variance"]
        ),

        (
            profile.flight_variance,
            current_features["flight_variance"]
        ),

        (
            profile.typing_speed,
            current_features["typing_speed"]
        )

    ]

    similarities = []

    for stored, current in features:

        if stored == 0:

            similarities.append(100)

            continue

        difference = abs(stored - current)

        percent_difference = difference / abs(stored)

        similarity = max(
            0,
            100 - (percent_difference * 100)
        )

        similarities.append(similarity)

    overall_similarity = sum(similarities) / len(similarities)

    return round(overall_similarity, 2)