def supervisor_decision(analysis: dict) -> dict:
    """
    Supervisor logic for Fraud Triage.
    """

    if analysis.get("fraud_risk") == "HIGH":
        return {
            "decision": "ESCALATE",
            "reason": "High fraud risk detected"
        }

    if analysis.get("fraud_risk") == "LOW" and analysis.get("entity_risk") == "LOW":
        return {
            "decision": "CLOSE",
            "reason": "Low fraud risk and clean history"
        }

    return {
        "decision": "REVIEW",
        "reason": "Moderate fraud indicators"
    }

