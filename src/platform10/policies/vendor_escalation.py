def requires_human_escalation(analysis: dict) -> bool:
    """
    Escalation rules for Vendor Onboarding.
    """

    if analysis.get("compliance_status") == "REVIEW_REQUIRED":
        return True

    if analysis.get("risk_score", 0) >= 60:
        return True

    return False

