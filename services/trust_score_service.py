def calculate_trust_score(similarity_score):
    """
    Convert similarity score into
    Trust Score and Risk Level.
    """

    similarity_score = max(0, min(100, similarity_score))

    if similarity_score >= 90:
        risk = "LOW"

    elif similarity_score >= 70:
        risk = "MEDIUM"

    else:
        risk = "HIGH"

    return {
        "trust_score": round(similarity_score, 2),
        "risk_level": risk
    }