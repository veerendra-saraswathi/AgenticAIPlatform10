# src/platform10/_dev/retry_pipeline_test.py

from platform10.runtime.executor import AgentExecutor
from platform10.runtime.engine import WorkflowEngine
from platform10.governance.audit_log import AuditLogger

from platform10.patterns.sequence import AgentPipeline, PipelineStep
from platform10.patterns.retry import RetryPolicy

from platform10.agents.flaky_agent import FlakyAgent
from platform10.agents.fallback_agent import FallbackAgent


def main():
    engine = WorkflowEngine(
        executor=AgentExecutor(),
        audit_logger=AuditLogger(),
    )

    pipeline = AgentPipeline(
        engine=engine,
        steps=[
            PipelineStep(
                name="flaky_step",
                agent=FlakyAgent(),
                retry_policy=RetryPolicy(
                    retries=3,
                    retry_delay_sec=0.2,
                    fallback_agent=FallbackAgent(),
                ),
                stop_on_failure=False,
            )
        ],
    )

    result = pipeline.run({"request_id": "123"})

    print("\n=== RETRY PIPELINE RESULT ===")
    print(result)


if __name__ == "__main__":
    main()
