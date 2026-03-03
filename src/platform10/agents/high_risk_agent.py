class HighRiskAgent:
    name = "high-risk-agent"

    def run(self, context):
        return {"decision": "manual-review-required"}
