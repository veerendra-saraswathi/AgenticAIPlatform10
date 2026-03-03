from typing import List, Dict


def aggregate_confidence(signals: List[Dict[str, float]]) -> float:
    """
    Weighted confidence aggregation.

    Used to justify decisions to:
    - risk teams
    - regulators
    """

    if not signals:
        return 0.0

    total_weight = 0.0
    weighted_sum = 0.0

    for s in signals:
        weighted_sum += s["confidence"] * s.get("weight", 1.0)
        total_weight += s.get("weight", 1.0)

    return round(weighted_sum / total_weight, 3)

