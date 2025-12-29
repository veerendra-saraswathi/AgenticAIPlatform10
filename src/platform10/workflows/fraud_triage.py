from typing import List, Dict, Any

from platform10.contracts.fraud_case import FraudCase
from platform10.contracts.fraud_decision import FraudDecision

from platform10.agents.location_signal_agent import LocationSignalAgent
from platform10.agents.velocity_signal_agent import VelocitySignalAgent
from platform10.agents.fraud_signal_agent import FraudSignalAgent
from platform10.agents.vendor_risk_agent import VendorRiskAgent
from platform10.agents.time_window_signal_agent import TimeWindowSignalAgent
from platform10.agents.customer_tenure_signal_agent import CustomerTenureSignalAgent

from platform10.governance.fraud.supervisor import supervisor_decision
from platform10.governance.human_review import request_human_review
from platform10.governance.audit_log import AuditLogger


_audit_logger = AuditLogger()


def _signals_to_analysis(signals: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Translate signal list into analysis dict expected by supervisor.
    """
    analysis: Dict[str, Any] = {}

    for s in signals:
        agent = s.get("agent")
        risk = s.get("risk")

        if agent == "location-signal-agent":
            analysis["geo_risk"] = risk
        elif agent == "velocity-signal-agent":
            analysis["velocity_risk"] = risk
        elif agent == "fraud-signal-agent":
            analysis["fraud_risk"] = risk
        elif agent == "vendor-risk-agent":
            analysis["vendor_risk"] = risk
        elif agent == "time-window-signal-agent":
            analysis["time_window_risk"] = risk
        elif agent == "customer-tenure-signal-agent":
            analysis["customer_tenure_risk"] = risk

    return analysis


def _compute_risk_score(analysis: Dict[str, Any]) -> float:
    """
    Simple additive risk score.
    """
    score = 0.0
    for v in analysis.values():
        if v == "HIGH":
            score += 1.0
    return score


def run_fraud_triage(case: FraudCase) -> FraudDecision:
    """
    End-to-end fraud triage workflow.
    """

    # --- Audit: start ---
    _audit_logger.record(
        execution_id=case.case_id,
        agent=type("Workflow", (), {"name": "fraud-triage-workflow"})(),
        input_context={
            "transaction": case.transaction,
            "context": case.context,
        },
        output={},
        status="STARTED",
    )

    # --- Instantiate agents ---
    location_agent = LocationSignalAgent()
    velocity_agent = VelocitySignalAgent()
    fraud_agent = FraudSignalAgent()
    vendor_agent = VendorRiskAgent()
    time_window_agent = TimeWindowSignalAgent()
    customer_tenure_agent = CustomerTenureSignalAgent()

    # --- Execute agents ---
    signals: List[Dict[str, Any]] = []

    for agent in [
        location_agent,
        velocity_agent,
        fraud_agent,
        vendor_agent,
        time_window_agent,
        customer_tenure_agent,
    ]:
        result = agent.evaluate(case)
        signals.append(result)

        _audit_logger.record(
            execution_id=case.case_id,
            agent=agent,
            input_context=case.transaction,
            output=result,
            status="SUCCESS",
        )

    # --- Normalize signals for policy ---
    analysis = _signals_to_analysis(signals)

    _audit_logger.record(
        execution_id=case.case_id,
        agent=type("Workflow", (), {"name": "fraud-triage-workflow"})(),
        input_context={"signals": signals},
        output={"analysis": analysis},
        status="ANALYSIS_COMPLETE",
    )

    # --- Supervisor decision ---
    recommendation = supervisor_decision(analysis)
    risk_score = _compute_risk_score(analysis)

    decision = recommendation["decision"]
    reason = recommendation["reason"]

    status = (
        "PENDING_HUMAN_REVIEW"
        if decision == "PENDING"
        else "AUTO_RESOLVED"
    )

    # --- Human-in-the-loop ---
    if decision == "PENDING":
        request_human_review(
            {
                "case_id": case.case_id,
                "analysis": analysis,
                "signals": signals,
            }
        )

    # --- Final audit ---
    _audit_logger.record(
        execution_id=case.case_id,
        agent=type("Workflow", (), {"name": "fraud-triage-workflow"})(),
        input_context={},
        output={
            "decision": decision,
            "risk_score": risk_score,
            "status": status,
            "reason": reason,
        },
        status="COMPLETED",
    )

    return FraudDecision(
        case_id=case.case_id,
        decision=decision,
        risk_score=risk_score,
        signals=signals,
        explanation=(
            f"Decision: {decision}\n"
            f"Risk score: {risk_score}\n"
            f"Signals:\n"
            + "\n".join(
                f"- {s['agent']} → {s['risk']}"
                for s in signals
            )
        ),
    )
