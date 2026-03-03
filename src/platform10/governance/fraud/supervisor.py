def supervisor_decision(analysis: dict) -> dict:
    """
    Supervisor policy for fraud triage decisions.
    """

    high_signals = [
        k for k, v in analysis.items()
        if v == "HIGH"
    ]

    if len(high_signals) >= 2:
        return {
            "decision": "PENDING",
            "reason": "Multiple high-risk indicators detected"
        }

    if len(high_signals) == 1:
        return {
            "decision": "REVIEW",
            "reason": "Single high-risk indicator detected"
        }

    return {
        "decision": "CLEAR",
        "reason": "No significant fraud indicators"
    }


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

