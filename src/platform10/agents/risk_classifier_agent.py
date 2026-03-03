"""
Risk Classifier Agent.

Aggregates fraud signals and determines overall risk level.
Enterprise-safe: preserves execution context.
"""

from typing import Dict, Any


class RiskClassifierAgent:
    name = "risk-classifier-agent"

    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Reads accumulated signals and assigns overall risk.
        Must preserve execution context.
        """

        signals = context.get("signals", [])

        high_count = 0
        medium_count = 0

        for signal in signals:
            risk = signal.get("risk")

            if risk == "HIGH":
                high_count += 1
            elif risk == "MEDIUM":
                medium_count += 1

        # Simple deterministic policy
        if high_count >= 1:
            overall_risk = "HIGH"
        elif medium_count >= 1:
            overall_risk = "MEDIUM"
        else:
            overall_risk = "LOW"

        # ✅ Preserve context — do NOT overwrite it
        context["risk"] = overall_risk
        context["risk_summary"] = {
            "high_signals": high_count,
            "medium_signals": medium_count,
            "total_signals": len(signals),
        }

        return context
        