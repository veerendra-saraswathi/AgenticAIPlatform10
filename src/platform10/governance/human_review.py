def request_human_review(state: dict) -> dict:
    state["human_required"] = True
    state["status"] = "PENDING_HUMAN_REVIEW"
    return state
