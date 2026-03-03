# src/platform10/memory/semantic_memory.py

from typing import Dict, Any


class SemanticMemory:
    """
    Stores abstracted knowledge and learned patterns.
    """

    def __init__(self):
        self.knowledge_base: Dict[str, Any] = {}

    def store_fact(self, key: str, value: Any) -> None:
        self.knowledge_base[key] = value

    def retrieve_fact(self, key: str) -> Any:
        return self.knowledge_base.get(key)

    def all_facts(self) -> Dict[str, Any]:
        return self.knowledge_base

    def total_facts(self) -> int:
        return len(self.knowledge_base)