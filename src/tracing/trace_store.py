from __future__ import annotations

import json
import os
from typing import Any, Dict


class TraceStore:
    """
    Filesystem-based trace persistence.

    This is intentionally simple and deterministic.
    Can later be swapped with DB / OpenTelemetry exporters.
    """

    def __init__(self, base_dir: str = "data/traces"):
        self.base_dir = base_dir
        self.workflow_dir = os.path.join(base_dir, "workflows")
        self.agent_dir = os.path.join(base_dir, "agents")

        os.makedirs(self.workflow_dir, exist_ok=True)
        os.makedirs(self.agent_dir, exist_ok=True)

    # ---------- workflow traces ----------

    def write_workflow_trace(
        self,
        workflow_execution_id: str,
        payload: Dict[str, Any],
    ) -> str:
        """
        Persist a workflow trace as JSON.

        Returns path to the written file.
        """
        path = os.path.join(
            self.workflow_dir,
            f"{workflow_execution_id}.json",
        )

        self._atomic_write(path, payload)
        return path

    # ---------- agent traces ----------

    def write_agent_trace(
        self,
        execution_id: str,
        payload: Dict[str, Any],
    ) -> str:
        """
        Persist an agent trace as JSON.
        """
        path = os.path.join(
            self.agent_dir,
            f"{execution_id}.json",
        )

        self._atomic_write(path, payload)
        return path

    # ---------- internals ----------

    def _atomic_write(self, path: str, payload: Dict[str, Any]) -> None:
        """
        Write JSON atomically to avoid partial writes.
        """
        tmp_path = f"{path}.tmp"

        with open(tmp_path, "w") as f:
            json.dump(payload, f, indent=2)

        os.replace(tmp_path, path)
