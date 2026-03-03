"""
Fraud Signal Agent
-----------------
Provides:
- Class-based agent (platform standard)
- Functional adapter (legacy workflows)
"""

class FraudSignalAgent:
    def run(self, context: dict) -> dict:
        """
        Analyze fraud-related signals and return structured risk output.
        """

        tx_count = context.get("tx_count", 0)
        country = context.get("country")

        fraud_score = 0.0

        # High transaction volume risk
        if tx_count > 10:
            fraud_score += 0.6

        # High-risk country
        if country in {"RU", "NG"}:
            fraud_score += 0.5

        # Cap score at 1.0
        fraud_score = min(fraud_score, 1.0)

        fraud_risk = "HIGH" if fraud_score >= 0.8 else "LOW"

        # Confidence inversely related to ambiguity
        confidence = 0.9 if fraud_score in {0.0, 1.0} else 0.6

        return {
            "fraud_score": fraud_score,
            "confidence": confidence,
            "fraud_risk": fraud_risk,
        }


# 🔁 FUNCTIONAL ADAPTER FOR WORKFLOWS
def analyze_fraud_signals(context: dict) -> dict:
    return FraudSignalAgent().run(context)