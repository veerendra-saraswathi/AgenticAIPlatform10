from platform10.workflows.vendor_onboarding import run_vendor_onboarding
from platform10.workflows.fraud_triage import run_fraud_triage


if __name__ == "__main__":
    print("\n--- VENDOR ONBOARDING ---")
    vendor = {
        "name": "Acme Payments Ltd",
        "regulated": True,
        "base_risk_score": 72,
        "fraud_signals": 1
    }
    print(run_vendor_onboarding(vendor))

    print("\n--- FRAUD TRIAGE ---")
    alert = {
        "transaction_id": "txn_123",
        "fraud_score": 78,
        "historical_risk": 45,
        "regulated_transaction": True
    }
    print(run_fraud_triage(alert))
