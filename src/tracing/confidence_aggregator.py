from typing import List, Optional
from dataclasses import dataclass


@dataclass
class ConfidenceSignal:
    agent: str
    confidence: float
    weight: float


class ConfidenceAggregator:
    """
    Deterministic confidence aggregation.
    """

    @staticmethod
    def weighted_mean(
        signals: List[ConfidenceSignal],
    ) -> Optional[float]:
        """
        Compute weighted mean confidence.
        Returns None if no valid signals.
        """
        if not signals:
            return None

        total_weight = sum(s.weight for s in signals)
        if total_weight == 0:
            return None

        weighted_sum = sum(
            s.confidence * s.weight for s in signals
        )

        return round(weighted_sum / total_weight, 4)
