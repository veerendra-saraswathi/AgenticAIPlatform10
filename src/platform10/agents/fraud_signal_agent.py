def analyze_fraud_signals(alert: dict) -> dict:
    """
    Analyzes raw fraud alert signals.
    """
    score = alert.get("fraud_score", 0)

    return {
        "fraud_score": score,
        "fraud_risk": (
            "HIGH" if score >= 80 else
            "MEDIUM" if score >= 50 else
            "LOW"
        )
    }
