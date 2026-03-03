# src/platform10/_dev/parallel_fanout_test.py

from platform10.runtime.executor import AgentExecutor
from platform10.runtime.engine import WorkflowEngine
from platform10.governance.audit_log import AuditLogger

from platform10.patterns.parallel import ParallelFanOut, ParallelStep

from platform10.agents.velocity_signal_agent import VelocitySignalAgent
from platform10.agents.location_signal_agent import LocationSignalAgent


def main():
    engine = WorkflowEngine(
        executor=AgentExecutor(),
        audit_logger=AuditLogger(),
    )

    parallel = ParallelFanOut(
        engine=engine,
        steps=[
            ParallelStep(
                name="velocity",
                agent=VelocitySignalAgent(),
            ),
            ParallelStep(
                name="location",
                agent=LocationSignalAgent(),
            ),
        ],
    )

    result = parallel.run(
        {
            "tx_count": 72,
            "country": "RU",
        }
    )

    print("\n=== PARALLEL FAN-OUT RESULT ===")
    print(result)


if __name__ == "__main__":
    main()
