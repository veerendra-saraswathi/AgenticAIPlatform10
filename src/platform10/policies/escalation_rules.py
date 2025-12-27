def requires_human_escalation(analysis: dict) -> bool:
    if analysis.get("fraud_risk") == "HIGH":
        return True

    if analysis.get("entity_risk") == "HIGH":
        return True

    if analysis.get("compliance_flag") == "REVIEW_REQUIRED":
        return True

    return False
