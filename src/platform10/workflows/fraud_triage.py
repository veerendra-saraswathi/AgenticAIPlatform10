"""
Fraud Triage Workflow
Runtime-aligned version using ExecutionEngine + run()
"""

import uuid

from platform10.runtime.engine import ExecutionEngine
from platform10.patterns.reflection import reflect, ReflectionFailed
from platform10.patterns.confidence import aggregate_confidence
from platform10.governance.replay.regulator_replay import replay_trace
from platform10.governance.audit_log import get_audit_log

from platform10.agents.fraud_signal_agent import FraudSignalAgent
from platform10.agents.velocity_signal_agent import VelocitySignalAgent
from platform10.agents.location_signal_agent import LocationSignalAgent
from platform10.agents.vendor_risk_agent import VendorRiskAgent
from platform10.agents.risk_classifier_agent import RiskClassifierAgent


def build_agents():
    return [
        FraudSignalAgent(),
        VelocitySignalAgent(),
        LocationSignalAgent(),
        VendorRiskAgent(),
        RiskClassifierAgent(),
    ]


def primary_decision(context):
    return context


def validator_fn(result, original_context):
    return True  # keep reflection simple for now


def extract_confidence_signals(context):
    signals = []
    for key, value in context.items():
        if isinstance(value, dict) and "confidence" in value:
            signals.append(value)
    return signals


def run_demo():
    print("\n=== AgenticAIPlatform10 :: Fraud Triage Demo ===\n")

    trace_id = str(uuid.uuid4())

    # 🔑 FLAT RUNTIME CONTEXT (what agents expect)
    input_data = {
        "case_id": "CASE-001",
        "tx_count": 12,
        "country": "NG",
        "amount": 250000,
        "velocity": 9.5,
        "customer_tenure_months": 2,
        "vendor_id": "VEND-777",
    }

    engine = ExecutionEngine()
    agents = build_agents()

    final_context = engine.execute_sequence(
        agents=agents,
        initial_input=input_data,
        trace_id=trace_id,
    )

    # --- Reflection ---
    try:
        reflected_result = reflect(
            primary_fn=primary_decision,
            validator_fn=validator_fn,
            context=final_context,
        )
        reflection_status = "PASSED"
    except ReflectionFailed as e:
        reflected_result = final_context
        reflection_status = f"FAILED: {str(e)}"

    # --- Confidence ---
    confidence_signals = extract_confidence_signals(reflected_result)
    overall_confidence = aggregate_confidence(confidence_signals)

    # --- Replay ---
    audit_backend = get_audit_log()
    replay = replay_trace(trace_id, audit_backend)

    print("Trace ID:", trace_id)
    print("\nFinal Context:")
    print(reflected_result)
    print("\nReflection Status:", reflection_status)
    print("\nOverall Confidence:", overall_confidence)
    print("\nReplay Steps:", len(replay.steps))
    print("Replay Final Decision:", replay.final_decision)

    print("\n=== Demo Complete ===\n")


if __name__ == "__main__":
    run_demo()