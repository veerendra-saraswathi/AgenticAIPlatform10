def check_compliance(alert: dict) -> dict:
    """
    Checks if alert involves regulated transaction types.
    """
    if alert.get("regulated_transaction", False):
        return {"compliance_flag": "REVIEW_REQUIRED"}

    return {"compliance_flag": "CLEAR"}
