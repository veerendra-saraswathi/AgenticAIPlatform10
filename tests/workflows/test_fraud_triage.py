from platform10.workflows.fraud_triage import run_fraud_triage


def test_fraud_never_auto_approves():
    """
    Fraud triage must never auto-approve alerts.
    """
    alert = {
        "transaction_id": "txn_test",
        "fraud_score": 10,
        "historical_risk": 10,
        "regulated_transaction": False
    }

    result = run_fraud_triage(alert)

    assert result["decision"] != "APPROVE"
    assert result["decision"] in {"CLOSE", "REVIEW", "PENDING"}


def test_fraud_high_risk_escalates():
    """
    High fraud risk must trigger human review.
    """
    alert = {
        "transaction_id": "txn_high",
        "fraud_score": 95,
        "historical_risk": 80,
        "regulated_transaction": True
    }

    result = run_fraud_triage(alert)

    assert result["status"] == "PENDING_HUMAN_REVIEW"
    assert result.get("human_required") is True


def test_fraud_has_audit_log():
    """
    Every fraud decision must produce an audit log.
    """
    alert = {
        "transaction_id": "txn_audit",
        "fraud_score": 60,
        "historical_risk": 40,
        "regulated_transaction": False
    }

    result = run_fraud_triage(alert)

    assert "audit_log" in result
    assert "analysis" in result["audit_log"]

