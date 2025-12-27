def supervisor_decision(analysis: dict) -> dict:
    """
    Supervisor logic for Vendor Onboarding.
    """

    if analysis.get("compliance_status") == "REVIEW_REQUIRED":
        return {
            "decision": "ESCALATE",
            "reason": "Compliance review required"
        }

    if analysis.get("risk_score", 0) >= 85:
        return {
            "decision": "REJECT",
            "reason": "Vendor risk score exceeds threshold"
        }

    return {
        "decision": "APPROVE",
        "reason": "Risk and compliance acceptable"
    }

