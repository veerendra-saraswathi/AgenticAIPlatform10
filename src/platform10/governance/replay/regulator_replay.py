"""
Regulator Replay Module.

Step-level deterministic replay with:
- Deep isolation
- SHA256 integrity hashing
- Append-only hash chain (ledger-style)
"""

import json
import os
import hashlib
from datetime import datetime
from typing import Dict, Any, List


class RegulatorReplay:
    STORAGE_DIR = "replay_logs"

    def __init__(self):
        os.makedirs(self.STORAGE_DIR, exist_ok=True)

    # ----------------------------
    # Utility: Deterministic Hash
    # ----------------------------

    def _compute_hash(self, payload: Dict[str, Any]) -> str:
        serialized = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

        return hashlib.sha256(serialized).hexdigest()

    # ----------------------------
    # Utility: Get Last Hash
    # ----------------------------

    def _get_last_integrity_hash(self) -> str:
        files = sorted(os.listdir(self.STORAGE_DIR))

        if not files:
            return "GENESIS"

        latest_file = files[-1]
        latest_path = os.path.join(self.STORAGE_DIR, latest_file)

        with open(latest_path, "r") as f:
            data = json.load(f)

        return data.get("integrity_hash", "GENESIS")

    # ----------------------------
    # Record Execution
    # ----------------------------

    def record(
        self,
        trace_id: str,
        input_snapshot: Dict[str, Any],
        steps: List[Dict[str, Any]],
        final_context: Dict[str, Any],
    ) -> None:

        file_path = os.path.join(
            self.STORAGE_DIR,
            f"{trace_id}.json",
        )

        previous_hash = self._get_last_integrity_hash()

        base_payload = {
            "trace_id": trace_id,
            "timestamp": datetime.utcnow().isoformat(),
            "previous_hash": previous_hash,
            "input_snapshot": input_snapshot,
            "steps": steps,
            "final_context": final_context,
        }

        integrity_hash = self._compute_hash(base_payload)

        payload = {
            **base_payload,
            "integrity_hash": f"sha256:{integrity_hash}",
        }

        with open(file_path, "w") as f:
            json.dump(payload, f, indent=2, sort_keys=True)

    # ----------------------------
    # Verify Single File
    # ----------------------------

    def verify(self, trace_id: str) -> bool:

        file_path = os.path.join(
            self.STORAGE_DIR,
            f"{trace_id}.json",
        )

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No replay found for {trace_id}")

        with open(file_path, "r") as f:
            stored_payload = json.load(f)

        stored_hash = stored_payload.pop("integrity_hash", None)

        if not stored_hash:
            return False

        expected_hash = self._compute_hash(stored_payload)

        return stored_hash == f"sha256:{expected_hash}"

    # ----------------------------
    # Verify Entire Chain
    # ----------------------------

    def verify_chain(self) -> bool:
        files = sorted(os.listdir(self.STORAGE_DIR))

        previous_hash = "GENESIS"

        for file in files:
            path = os.path.join(self.STORAGE_DIR, file)

            with open(path, "r") as f:
                payload = json.load(f)

            stored_hash = payload.get("integrity_hash")
            stored_previous = payload.get("previous_hash")

            if stored_previous != previous_hash:
                return False

            payload_copy = payload.copy()
            payload_copy.pop("integrity_hash", None)

            expected_hash = self._compute_hash(payload_copy)

            if stored_hash != f"sha256:{expected_hash}":
                return False

            previous_hash = stored_hash

        return True
        