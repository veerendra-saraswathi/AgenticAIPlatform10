"""
Anomaly Detection Model (Stub)
------------------------------
ML-ready interface for infrastructure anomaly detection.

Phase-0:
- Simple heuristic wrapped as a model
Phase-1:
- Replace with trained ML/DL model
"""

class AnomalyDetectionModel:
    def __init__(self):
        """
        In real systems:
        - Load model weights
        - Load scalers / feature config
        """
        pass

    def predict(self, features: dict) -> dict:
        """
        Predict anomaly probability.

        Returns:
        {
            "anomaly": bool,
            "confidence": float
        }
        """
        temperature = features.get("temperature", 0)
        vibration = features.get("vibration", 0)

        score = 0.0

        if temperature > 80:
            score += 0.6
        if vibration > 7:
            score += 0.4

        anomaly = score >= 0.7

        return {
            "anomaly": anomaly,
            "confidence": round(score, 2),
        }

