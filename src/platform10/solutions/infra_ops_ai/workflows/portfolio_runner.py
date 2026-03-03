"""
Portfolio Runner
----------------
Executes InfraOps workflow across a portfolio of assets.
"""

from platform10.solutions.infra_ops_ai.workflows.infra_ops_workflow import (
    InfraOpsWorkflow,
)


class InfraOpsPortfolioRunner:
    """
    Runs infra-ops workflow across multiple assets.
    """

    def __init__(self):
        self.workflow = InfraOpsWorkflow().build()

    def run(self, assets: list[dict]) -> dict:
        results = []
        summary = {
            "total_assets": len(assets),
            "autonomous_actions": 0,
            "human_reviews": 0,
            "no_actions": 0,
        }

        for asset_context in assets:
            result = self.workflow.run(asset_context)
            results.append(result)

            action = result.get("maintenance_action")
            if action == "DISPATCH_MAINTENANCE":
                summary["autonomous_actions"] += 1
            elif action == "HUMAN_REVIEW_REQUIRED":
                summary["human_reviews"] += 1
            else:
                summary["no_actions"] += 1

        return {
            "portfolio_summary": summary,
            "asset_results": results,
        }

