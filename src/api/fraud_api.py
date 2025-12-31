from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

from workflows.fraud_triage_workflow import (
    run_fraud_triage_workflow,
)

router = APIRouter(prefix="/fraud", tags=["fraud"])


# -----------------------------
# Request / Response Models
# -----------------------------

class FraudTriageRequest(BaseModel):
    transaction: Dict[str, Any]
    context: Dict[str, Any] = {}


class FraudTriageResponse(BaseModel):
    decision: str
    confidence: float | None
    workflow_execution_id: str


# -----------------------------
# API Endpoint
# -----------------------------

@router.post(
    "/triage",
    response_model=FraudTriageResponse,
)
def fraud_triage(
    request: FraudTriageRequest,
):
    """
    Run fraud triage workflow.
    """

    inputs = {
        **request.transaction,
        **request.context,
    }

    result = run_fraud_triage_workflow(inputs)

    return FraudTriageResponse(**result)
