import os
from platform10.observability.pii_masking import mask_pii

TRACE_DIR = "data/agent_traces"
os.makedirs(TRACE_DIR, exist_ok=True)


def persist_trace(trace):
    """
    Persist agent trace with PII masked.
    """
    safe_trace_dict = {
        "execution_id": trace.execution_id,
        "agent_name": trace.agent_name,
        "task_type": trace.task_type,
        "inputs": mask_pii(trace.inputs),
        "signals": mask_pii(trace.signals),
        "decision": trace.decision,
        "reasoning": trace.reasoning,
        "confidence": trace.confidence,
        "outcome": trace.outcome,
        "timestamp": trace.timestamp,
    }

    path = f"{TRACE_DIR}/{trace.execution_id}.json"
    with open(path, "w") as f:
        import json
        json.dump(safe_trace_dict, f, indent=2)

