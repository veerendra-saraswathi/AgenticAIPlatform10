from typing import Dict, Any

# --- tracing imports ---
from tracing.workflow_trace import WorkflowTrace
from tracing.agent_trace import AgentTrace
from tracing.trace_store import TraceStore
from tracing.confidence_aggregator import (
    ConfidenceAggregator,
    ConfidenceSignal,
)

# --- import your real agents here ---
# Example:
# from agents.velocity_agent import velocity_agent
# from agents.location_agent import location_agent
# from agents.behaviour_agent import behaviour_agent


def run_fraud_triage_workflow(
    inputs: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Canonical fraud triage workflow.

    This is the ONLY place where:
    - agents are orchestrated
    - traces are collected
    - confidence is aggregated
    """

    trace_store = TraceStore()

    # -------------------------------------------------
    # 1️⃣ Start workflow trace
    # -------------------------------------------------
    workflow_trace = WorkflowTrace.start(
        workflow_name="fraud-triage-workflow"
    )

    # -------------------------------------------------
    # 2️⃣ Velocity Agent
    # -------------------------------------------------
    velocity_trace = AgentTrace.start(
        agent_name="velocity-signal-agent",
        task_type="fraud_signal_detection",
        inputs=inputs,
    )

    velocity_result = velocity_agent.run(inputs)

    velocity_trace.record_signals(
        velocity_result.get("signals", {})
    )

    velocity_trace.finalize(
        decision=velocity_result.get("decision"),
        reasoning=velocity_result.get("reasoning"),
        confidence=velocity_result.get("confidence"),
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
    # 3️⃣ Location Agent
    # -------------------------------------------------
    location_trace = AgentTrace.start(
        agent_name="location-signal-agent",
        task_type="fraud_signal_detection",
        inputs=inputs,
    )

    location_result = location_agent.run(inputs)

    location_trace.record_signals(
        location_result.get("signals", {})
    )

    location_trace.finalize(
        decision=location_result.get("decision"),
        reasoning=location_result.get("reasoning"),
        confidence=location_result.get("confidence"),
    )

    trace_store.write_agent_trace(
        location_trace.execution_id,
        location_trace.to_dict(),
    )

    workflow_trace.record_agent_result(
        agent_name=location_trace.agent_name,
        execution_id=location_trace.execution_id,
        decision=location_trace.decision,
        confidence=location_trace.confidence,
    )

    # -------------------------------------------------
    # 4️⃣ Behaviour Agent
    # -------------------------------------------------
    behaviour_trace = AgentTrace.start(
        agent_name="behaviour-signal-agent",
        task_type="fraud_signal_detection",
        inputs=inputs,
    )

    behaviour_result = behaviour_agent.run(inputs)

    behaviour_trace.record_signals(
        behaviour_result.get("signals", {})
    )

    behaviour_trace.finalize(
        decision=behaviour_result.get("decision"),
        reasoning=behaviour_result.get("reasoning"),
        confidence=behaviour_result.get("confidence"),
    )

    trace_store.write_agent_trace(
        behaviour_trace.execution_id,
        behaviour_trace.to_dict(),
    )

    workflow_trace.record_agent_result(
        agent_name=behaviour_trace.agent_name,
        execution_id=behaviour_trace.execution_id,
        decision=behaviour_trace.decision,
        confidence=behaviour_trace.confidence,
    )

    # -------------------------------------------------
    # 5️⃣ Confidence aggregation
    # -------------------------------------------------
    signals = [
        ConfidenceSignal(
            agent="velocity-signal-agent",
            confidence=velocity_trace.confidence,
            weight=0.4,
        ),
        ConfidenceSignal(
            agent="location-signal-agent",
            confidence=location_trace.confidence,
            weight=0.35,
        ),
        ConfidenceSignal(
            agent="behaviour-signal-agent",
            confidence=behaviour_trace.confidence,
            weight=0.25,
        ),
    ]

    final_confidence = ConfidenceAggregator.weighted_mean(
        signals
    )

    # -------------------------------------------------
    # 6️⃣ Final decision policy
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
    # 7️⃣ Finalize workflow trace
    # -------------------------------------------------
    workflow_trace.finalize(
        final_decision=final_decision,
        final_confidence=final_confidence,
        explainability={
            "aggregation": "weighted_mean",
            "weights": {
                "velocity": 0.4,
                "location": 0.35,
                "behaviour": 0.25,
            },
        },
        human_review_required=final_decision == "REVIEW",
    )

    trace_store.write_workflow_trace(
        workflow_trace.workflow_execution_id,
        workflow_trace.to_dict(),
    )

    # -------------------------------------------------
    # 8️⃣ Return result
    # -------------------------------------------------
    return {
        "decision": final_decision,
        "confidence": final_confidence,
        "workflow_execution_id": workflow_trace.workflow_execution_id,
    }
