def assess_vendor_risk(entity: dict) -> dict:
    """
    Evaluates historical risk of the entity involved in fraud alert.
    """
    history = entity.get("historical_risk", 0)

    return {
        "historical_risk": history,
        "entity_risk": (
            "HIGH" if history >= 70 else
            "MEDIUM" if history >= 40 else
            "LOW"
        )
    }
