from typing import Dict, Any
from platform10.patterns.base import AgenticPattern
from platform10.audit.logger import audit_log


def run_pattern(
    pattern: AgenticPattern,
    context: Dict[str, Any],
    execution_id: str
) -> Dict[str, Any]:

    audit_log({
        "execution_id": execution_id,
        "pattern": pattern.pattern_id,
        "event": "STARTED",
        "context": context
    })

    output = pattern.execute(context)

    audit_log({
        "execution_id": execution_id,
        "pattern": pattern.pattern_id,
        "event": "COMPLETED",
        "output": output
    })

    return output

