class RiskClassifierAgent:
    name = "risk-classifier-agent"

    def run(self, context):
        amount = context.get("amount", 0)

        if amount > 10_000:
            return {"risk": "HIGH"}
        return {"risk": "LOW"}
