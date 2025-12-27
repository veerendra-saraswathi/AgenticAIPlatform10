def record_audit_log(state: dict) -> dict:
    state["audit_log"] = {
        "decision": state.get("decision"),
        "reason": state.get("reason"),
        "inputs": state.get("vendor"),
        "analysis": state.get("analysis")
    }
    return state
