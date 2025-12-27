from platform10.agents.fraud_signal_agent import analyze_fraud_signals
from platform10.agents.vendor_risk_agent import assess_vendor_risk
from platform10.agents.compliance_agent import check_compliance

from platform10.policies.escalation_rules import requires_human_escalation
from platform10.governance.fraud.supervisor import supervisor_decision
from platform10.governance.human_review import request_human_review
from platform10.governance.audit_log import record_audit_log


def run_fraud_triage(alert: dict) -> dict:
    """
    Executes the Fraud Alert Triage workflow.
    """

    state = {
        "alert": alert
    }

    # --- Agent Analysis ---
    fraud = analyze_fraud_signals(alert)
    entity = assess_vendor_risk(alert)
    compliance = check_compliance(alert)

    analysis = {**fraud, **entity, **compliance}
    state["analysis"] = analysis

    # --- Supervisor Recommendation ---
    recommendation = supervisor_decision(analysis)
    state["recommendation"] = recommendation

    # --- Governance ---
    if requires_human_escalation(analysis):
        state["decision"] = "PENDING"
        state["reason"] = recommendation["reason"]
        state["status"] = "PENDING_HUMAN_REVIEW"
        state = request_human_review(state)
    else:
        state["decision"] = recommendation["decision"]
        state["reason"] = recommendation["reason"]
        state["status"] = "AUTO_RESOLVED"

    # --- Audit ---
    state = record_audit_log(state)
    return state
