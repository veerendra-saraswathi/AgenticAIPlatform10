from typing import Dict, Any

# ----------------------------
# Tracing & workflow infra
# ----------------------------
from tracing.workflow_trace import WorkflowTrace
from tracing.agent_trace import AgentTrace
from tracing.trace_store import TraceStore
from tracing.confidence_aggregator import (
    ConfidenceAggregator,
    ConfidenceSignal,
)

# ----------------------------
# Legacy agents & contracts
# ----------------------------
from platform10.agents.velocity_signal_agent import VelocitySignalAgent
from platform10.contracts.fraud_case import FraudCase


def run_fraud_triage_workflow(
    inputs: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Fraud triage workflow using real legacy agents
    with canonical tracing and confidence aggregation.
    """

    trace_store = TraceStore()

    # -------------------------------------------------
    # 1️⃣ Start workflow trace
    # -------------------------------------------------
    workflow_trace = WorkflowTrace.start(
        workflow_name="fraud-triage-workflow"
    )

    # -------------------------------------------------
    # 2️⃣ Instantiate agents (REAL)
    # -------------------------------------------------
    velocity_agent = VelocitySignalAgent()

    # -------------------------------------------------
    # 3️⃣ Velocity Signal Agent (REAL)
    # -------------------------------------------------
    velocity_trace = AgentTrace.start(
        agent_name="velocity-signal-agent",
        task_type="fraud_signal_detection",
        inputs=inputs,
    )

    fraud_case = FraudCase(
        case_id=workflow_trace.workflow_execution_id,
        transaction=inputs,
        context={},
    )

    velocity_signal = velocity_agent.evaluate(fraud_case)

    velocity_risk = velocity_signal.get("risk", "LOW")

    if velocity_risk == "HIGH":
        velocity_decision = "HIGH"
        velocity_confidence = 0.9
    elif velocity_risk == "MEDIUM":
        velocity_decision = "MEDIUM"
        velocity_confidence = 0.6
    else:
        velocity_decision = "LOW"
        velocity_confidence = 0.3

    velocity_trace.record_signals(velocity_signal)

    velocity_trace.finalize(
        decision=velocity_decision,
        reasoning=f"Transaction count = {velocity_signal.get('tx_count')}",
        confidence=velocity_confidence,
    )

    trace_store.write_agent_trace(
        velocity_trace.execution_id,
        velocity_trace.to_dict(),
    )

    workflow_trace.record_agent_result(
        agent_name=velocity_trace.agent_name,
        execution_id=velocity_trace.execution_id,
        decision=velocity_trace.decision,
        confidence=velocity_trace.confidence,
    )

    # -------------------------------------------------
    # 4️⃣ Confidence aggregation (single-agent for now)
    # -------------------------------------------------
    signals = [
        ConfidenceSignal(
            agent="velocity-signal-agent",
            confidence=velocity_confidence,
            weight=1.0,
        )
    ]

    final_confidence = ConfidenceAggregator.weighted_mean(signals)

    # -------------------------------------------------
    # 5️⃣ Final decision policy
    # -------------------------------------------------
    if final_confidence is None:
        final_decision = "REVIEW"
    elif final_confidence >= 0.85:
        final_decision = "HOLD_TRANSACTION"
    elif final_confidence >= 0.6:
        final_decision = "REVIEW"
    else:
        final_decision = "APPROVE"

    # -------------------------------------------------
    # 6️⃣ Finalize workflow trace
    # -------------------------------------------------
    workflow_trace.finalize(
        final_decision=final_decision,
        final_confidence=final_confidence,
        explainability={
            "aggregation": "weighted_mean",
            "agents": {
                "velocity": velocity_risk
            },
        },
        human_review_required=final_decision == "REVIEW",
    )

    trace_store.write_workflow_trace(
        workflow_trace.workflow_execution_id,
        workflow_trace.to_dict(),
    )

    # -------------------------------------------------
    # 7️⃣ Return API response
    # -------------------------------------------------
    return {
        "decision": final_decision,
        "confidence": final_confidence,
        "workflow_execution_id": workflow_trace.workflow_execution_id,
    }
