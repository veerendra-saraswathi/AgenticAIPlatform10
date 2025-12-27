from platform10.agents.vendor_risk_agent import assess_vendor_risk
from platform10.agents.compliance_agent import check_compliance
from platform10.agents.fraud_signal_agent import analyze_fraud_signals

from platform10.policies.vendor_escalation import requires_human_escalation
from platform10.governance.vendor.supervisor import supervisor_decision
from platform10.governance.human_review import request_human_review
from platform10.governance.audit_log import record_audit_log


def run_vendor_onboarding(vendor: dict) -> dict:
    """
    Vendor Onboarding Risk Assessment Workflow (Platform10).

    Produces:
    - analysis (facts)
    - recommendation (AI supervisor judgment)
    - decision (governed outcome)
    - human escalation if required
    - audit log
    """

    state = {
        "vendor": vendor
    }

    # ------------------------------------------------------------------
    # Agent Analysis (facts only, no decisions)
    # ------------------------------------------------------------------
    risk = assess_vendor_risk(vendor)
    compliance = check_compliance(vendor)
    fraud = analyze_fraud_signals(vendor)

    analysis = {
    **risk,
    **compliance,
    **fraud,
    "risk_score": vendor.get("base_risk_score", 0)
}

    state["analysis"] = analysis

    # ------------------------------------------------------------------
    # Supervisor Recommendation (AI judgment, not final authority)
    # ------------------------------------------------------------------
    recommendation = supervisor_decision(analysis)
    state["recommendation"] = recommendation

    # ------------------------------------------------------------------
    # Governance & Escalation (policy-enforced)
    # ------------------------------------------------------------------
    if requires_human_escalation(analysis):
        state["decision"] = "PENDING"
        state["reason"] = recommendation["reason"]
        state["status"] = "PENDING_HUMAN_REVIEW"
        state = request_human_review(state)
    else:
        state["decision"] = recommendation["decision"]
        state["reason"] = recommendation["reason"]
        state["status"] = "AUTO_APPROVED"

    # ------------------------------------------------------------------
    # Audit Log (mandatory for regulated workflows)
    # ------------------------------------------------------------------
    state = record_audit_log(state)

    return state
