"""
Agentic AI Platform CLI

Purpose:
- Entry point for running workflows
- Ensures trace_id continuity for audit & replay
"""

import json
import uuid
import argparse
from typing import Any, Dict

from platform10.workflows.fraud_triage import FraudTriageWorkflow
from platform10.governance.audit_log import get_audit_log
from platform10.governance.replay.regulator_replay import replay_trace


def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r") as f:
        return json.load(f)


def run_fraud_triage(input_path: str) -> None:
    trace_id = str(uuid.uuid4())

    workflow = FraudTriageWorkflow()
    case_data = load_json(input_path)

    result = workflow.run(case_data=case_data, trace_id=trace_id)

    print("\n=== FRAUD TRIAGE RESULT ===")
    print(json.dumps(result, indent=2))

    print("\nTRACE ID:")
    print(trace_id)


def replay_decision(trace_id: str) -> None:
    audit_log = get_audit_log()
    replay = replay_trace(trace_id, audit_log)

    print("\n=== DECISION REPLAY ===")
    print(f"Trace ID: {replay.trace_id}")
    print(f"Created At: {replay.created_at}")

    for step in replay.steps:
        print("\n--- STEP ---")
        print(f"Time: {step.timestamp}")
        print(f"Component: {step.component}")
        print(f"Action: {step.action}")
        print("Input:", step.input_data)
        print("Output:", step.output_data)

    print("\nFINAL DECISION:")
    print(replay.final_decision)


def main():
    parser = argparse.ArgumentParser(description="Agentic AI Platform CLI")

    subparsers = parser.add_subparsers(dest="command")

    run_cmd = subparsers.add_parser("run-fraud")
    run_cmd.add_argument("--input", required=True, help="Path to case JSON")

    replay_cmd = subparsers.add_parser("replay")
    replay_cmd.add_argument("--trace-id", required=True, help="Trace ID to replay")

    args = parser.parse_args()

    if args.command == "run-fraud":
        run_fraud_triage(args.input)
    elif args.command == "replay":
        replay_decision(args.trace_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
