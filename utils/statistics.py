from statistics import mean, variance


def calculate_mean(values):
    """
    Calculate the mean of a list.
    """
    if not values:
        return 0.0

    return mean(values)


def calculate_variance(values):
    """
    Calculate variance safely.
    """
    if len(values) < 2:
        return 0.0

    return variance(values)


def typing_speed(total_keys, duration_ms):
    """
    Calculate keys per second.
    """

    if duration_ms <= 0:
        return 0.0

    seconds = duration_ms / 1000

    return total_keys / seconds