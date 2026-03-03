# src/platform10/memory/episodic_memory.py

from datetime import datetime
from typing import Dict, Any, List


class EpisodicMemory:
    """
    Stores individual decision episodes with timestamps.
    """

    def __init__(self):
        self.episodes: List[Dict[str, Any]] = []

    def store_episode(self, event_type: str, data: Dict[str, Any]) -> None:
        episode = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "data": data,
        }
        self.episodes.append(episode)

    def get_recent(self, limit: int = 5) -> List[Dict[str, Any]]:
        return self.episodes[-limit:]

    def query_by_event(self, event_type: str) -> List[Dict[str, Any]]:
        return [e for e in self.episodes if e["event_type"] == event_type]

    def total_episodes(self) -> int:
        return len(self.episodes)
        