"""
Vendor Risk Agent
-----------------
Provides both:
- Class-based agent (platform standard)
- Functional adapter (legacy workflows)
"""

class VendorRiskAgent:
    def run(self, context: dict) -> dict:
        risk = "HIGH" if context.get("vendor_score", 0) > 70 else "LOW"
        return {"vendor_risk": risk}


# 🔁 FUNCTIONAL ADAPTER FOR WORKFLOWS
def assess_vendor_risk(context: dict) -> dict:
    return VendorRiskAgent().run(context)
