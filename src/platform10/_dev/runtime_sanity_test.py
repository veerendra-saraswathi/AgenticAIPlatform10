# src/platform10/_dev/runtime_sanity_test.py

from platform10.runtime.executor import AgentExecutor
from platform10.runtime.engine import WorkflowEngine
from platform10.governance.audit_log import AuditLogger
from platform10.agents.echo_agent import EchoAgent


def main():
    engine = WorkflowEngine(
        executor=AgentExecutor(),
        audit_logger=AuditLogger(),
    )

    result = engine.run_agent(
        agent=EchoAgent(),
        context={"hello": "world"},
    )

    print("\n=== FINAL RESULT ===")
    print(result)


if __name__ == "__main__":
    main()
