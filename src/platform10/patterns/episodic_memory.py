from typing import Dict, Any, List


class EpisodicMemory:
    """
    Stores past execution snapshots.

    Used for:
    - audits
    - investigations
    - regulator replay
    """

    def __init__(self):
        self._episodes: List[Dict[str, Any]] = []

    def record(self, episode: Dict[str, Any]):
        self._episodes.append(dict(episode))

    def recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self._episodes[-limit:]

