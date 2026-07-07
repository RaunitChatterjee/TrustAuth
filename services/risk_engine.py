def evaluate_risk(trust_score):
    """
    Convert a trust score into a
    banking risk level.
    """

    if trust_score is None:
        return {
            "risk_level": "UNKNOWN",
            "action": "ENROLLMENT_REQUIRED"
        }

    if trust_score >= 90:
        return {
            "risk_level": "LOW",
            "action": "ALLOW"
        }

    if trust_score >= 70:
        return {
            "risk_level": "MEDIUM",
            "action": "MONITOR"
        }

    if trust_score >= 40:
        return {
            "risk_level": "HIGH",
            "action": "STEP_UP_AUTH"
        }

    return {
        "risk_level": "CRITICAL",
        "action": "BLOCK"
    }