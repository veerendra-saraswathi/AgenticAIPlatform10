# src/platform10/patterns/reflection_pattern.py

"""
Reflection Pattern
Upgraded with Exponential Temporal Decay Weighting
"""

from typing import Dict, Any, List
from datetime import datetime
import math


class ReflectionPattern:
    """
    Reflection with:
    - Persistent memory awareness
    - Exponential temporal decay weighting
    """

    # Decay rate per hour (tunable)
    DECAY_LAMBDA = 0.15

    def __init__(self, memory_manager=None):
        self.memory = memory_manager

    def reflect(self, decision: Dict[str, Any]) -> Dict[str, Any]:

        fraud_score = decision.get("fraud_score", 0.0)
        confidence = decision.get("confidence", 0.0)
        verdict = decision.get("verdict", "UNKNOWN")

        historical_adjustment = 0.0
        pattern_flag = None

        # --------------------------------------------------
        # Exponential Temporal Decay Risk Density
        # --------------------------------------------------
        if self.memory:

            recent_events: List[Dict[str, Any]] = (
                self.memory.recall_by_type("fraud_assessment")
            )

            now = datetime.utcnow()

            weighted_high_risk = 0.0
            weighted_total = 0.0

            for event in recent_events:

                score = event["data"].get("score", 0.0)
                timestamp_str = event.get("timestamp")

                if not timestamp_str:
                    continue

                event_time = datetime.fromisoformat(timestamp_str)
                age_hours = (now - event_time).total_seconds() / 3600.0

                # Exponential decay
                weight = math.exp(-self.DECAY_LAMBDA * age_hours)

                weighted_total += weight

                if score >= 0.8:
                    weighted_high_risk += weight

            if weighted_total > 0:
                risk_density = weighted_high_risk / weighted_total

                historical_adjustment = -0.25 * risk_density

                if risk_density >= 0.5:
                    pattern_flag = "High Systemic Risk Environment"

        # --------------------------------------------------
        # Apply Adjustment
        # --------------------------------------------------
        adjusted_confidence = max(
            0.0,
            min(1.0, confidence + historical_adjustment),
        )

        return {
            "fraud_score": fraud_score,
            "original_confidence": confidence,
            "adjusted_confidence": adjusted_confidence,
            "verdict": verdict,
            "reflection_flag": pattern_flag,
        }
        