from platform10.workflows.vendor_onboarding import run_vendor_onboarding


def test_vendor_never_closes():
    """
    Vendor onboarding must never return CLOSE.
    """
    vendor = {
        "name": "Test Vendor",
        "regulated": True,
        "base_risk_score": 30,
        "fraud_signals": 0
    }

    result = run_vendor_onboarding(vendor)

    assert result["decision"] != "CLOSE"
    assert result["decision"] in {"APPROVE", "REJECT", "PENDING"}


def test_vendor_escalates_on_high_risk():
    """
    High-risk vendors must require human review.
    """
    vendor = {
        "name": "High Risk Vendor",
        "regulated": True,
        "base_risk_score": 80,
        "fraud_signals": 0
    }

    result = run_vendor_onboarding(vendor)

    assert result["status"] == "PENDING_HUMAN_REVIEW"
    assert result.get("human_required") is True


def test_vendor_has_audit_log():
    """
    Every vendor decision must produce an audit log.
    """
    vendor = {
        "name": "Audit Vendor",
        "regulated": True,
        "base_risk_score": 50,
        "fraud_signals": 1
    }

    result = run_vendor_onboarding(vendor)

    assert "audit_log" in result
    assert "analysis" in result["audit_log"]

