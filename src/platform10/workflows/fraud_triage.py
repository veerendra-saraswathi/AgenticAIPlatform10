"""
Fraud Triage Workflow Demo.

Demonstrates enterprise-grade, deterministic execution
with signal aggregation and decisioning.
"""

import uuid
from pprint import pprint

from platform10.runtime.engine import ExecutionEngine

from platform10.agents.velocity_signal_agent import VelocitySignalAgent
from platform10.agents.time_window_velocity_signal_agent import (
    TimeWindowVelocitySignalAgent,
)
from platform10.agents.location_signal_agent import LocationSignalAgent
from platform10.agents.risk_classifier_agent import RiskClassifierAgent


def run_demo():
    print("\n=== AgenticAIPlatform10 :: Fraud Triage Demo ===\n")

    trace_id = str(uuid.uuid4())

    # Sample input case
    input_case = {
        "case_id": "CASE-001",
        "transaction": {
            "amount": 25000,
            "currency": "INR",
            "tx_count": 35,
        },
        "context": {
            "tx_count_last_10_min": 12,
            "location_mismatch": True,
        },
    }

    # ✅ ENTERPRISE CONTEXT INITIALIZATION
    initial_input = {
        "case": input_case,
        "signals": [],
        "trace_id": trace_id,
    }

    agents = [
        VelocitySignalAgent(),
        TimeWindowVelocitySignalAgent(),
        LocationSignalAgent(),
        RiskClassifierAgent(),
    ]

    engine = ExecutionEngine()

    final_context = engine.execute_sequence(
        agents=agents,
        initial_input=initial_input,
        trace_id=trace_id,
    )

    print("=== FINAL EXECUTION CONTEXT ===")
    pprint(final_context)
    print()


if __name__ == "__main__":
    run_demo()
    