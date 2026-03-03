# src/platform10/_dev/conditional_routing_test.py

from platform10.runtime.executor import AgentExecutor
from platform10.runtime.engine import WorkflowEngine
from platform10.governance.audit_log import AuditLogger

from platform10.patterns.sequence import AgentPipeline, PipelineStep
from platform10.patterns.routing import ConditionalRouter, Route

from platform10.agents.risk_classifier_agent import RiskClassifierAgent
from platform10.agents.low_risk_agent import LowRiskAgent
from platform10.agents.high_risk_agent import HighRiskAgent


def main():
    engine = WorkflowEngine(
        executor=AgentExecutor(),
        audit_logger=AuditLogger(),
    )

    # ---- Decision pipeline ----
    decision_pipeline = AgentPipeline(
        engine,
        steps=[
            PipelineStep(
                name="risk_classification",
                agent=RiskClassifierAgent(),
            )
        ],
    )

    # ---- Low risk pipeline ----
    low_risk_pipeline = AgentPipeline(
        engine,
        steps=[
            PipelineStep(
                name="low_risk_decision",
                agent=LowRiskAgent(),
            )
        ],
    )

    # ---- High risk pipeline ----
    high_risk_pipeline = AgentPipeline(
        engine,
        steps=[
            PipelineStep(
                name="high_risk_decision",
                agent=HighRiskAgent(),
            )
        ],
    )

    router = ConditionalRouter(
        engine=engine,
        routes={
            "low_risk": Route(
                name="low_risk",
                condition=lambda ctx: ctx.get("risk_classification_output", {}).get("risk") == "LOW",
                pipeline=low_risk_pipeline,
            ),
            "high_risk": Route(
                name="high_risk",
                condition=lambda ctx: ctx.get("risk_classification_output", {}).get("risk") == "HIGH",
                pipeline=high_risk_pipeline,
            ),
        },
    )

    # ---- Execute decision first ----
    context = decision_pipeline.run({"amount": 25_000})["final_context"]

    # ---- Route based on decision ----
    result = router.run(context)

    print("\n=== CONDITIONAL ROUTING RESULT ===")
    print(result)


if __name__ == "__main__":
    main()
