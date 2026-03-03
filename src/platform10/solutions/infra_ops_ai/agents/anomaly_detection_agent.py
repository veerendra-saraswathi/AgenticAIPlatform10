"""
Anomaly Detection Agent (ML-backed)
----------------------------------
Uses an anomaly detection model to identify infrastructure risks.
"""

from platform10.solutions.infra_ops_ai.models.anomaly_model import (
    AnomalyDetectionModel,
)


class AnomalyDetectionAgent:
    def __init__(self):
        self.model = AnomalyDetectionModel()

    def run(self, context: dict) -> dict:
        """
        Run anomaly detection using ML model.
        """
        prediction = self.model.predict(context)

        return {
            "anomaly_detected": prediction["anomaly"],
            "anomaly_confidence": prediction["confidence"],
            "anomaly_reason": (
                "model_confidence_high"
                if prediction["anomaly"]
                else "model_confidence_low"
            ),
            "tokens": 10,  # ML inference cost (simulated)
        }
