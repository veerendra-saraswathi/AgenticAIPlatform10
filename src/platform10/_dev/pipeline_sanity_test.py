from platform10.runtime.executor import AgentExecutor
from platform10.runtime.engine import WorkflowEngine
from platform10.governance.audit_log import AuditLogger
from platform10.patterns.sequence import AgentPipeline, PipelineStep
from platform10.agents.uppercase_agent import UppercaseAgent
from platform10.agents.suffix_agent import SuffixAgent


def main():
    engine = WorkflowEngine(
        executor=AgentExecutor(),
        audit_logger=AuditLogger(),
    )

    pipeline = AgentPipeline(
        engine=engine,
        steps=[
            PipelineStep(
                name="uppercase",
                agent=UppercaseAgent(),
            ),
            PipelineStep(
                name="suffix",
                agent=SuffixAgent(),
            ),
        ],
    )

    result = pipeline.run({"text": "agentic ai"})
    print("\n=== PIPELINE RESULT ===")
    print(result)


if __name__ == "__main__":
    main()

