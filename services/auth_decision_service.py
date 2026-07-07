def make_authentication_decision(risk):
    """
    Decide what the banking application
    should do based on calculated risk.
    """

    level = risk["risk_level"]

    if level == "LOW":
        return {
            "decision": "ALLOW",
            "message": "Authentication successful."
        }

    if level == "MEDIUM":
        return {
            "decision": "MONITOR",
            "message": "Continue monitoring user behavior."
        }

    if level == "HIGH":
        return {
            "decision": "STEP_UP",
            "message": "Additional authentication required."
        }

    if level == "CRITICAL":
        return {
            "decision": "BLOCK",
            "message": "Potential Account Takeover detected."
        }

    return {
        "decision": "UNKNOWN",
        "message": "Unable to determine authentication state."
    }