from typing import Protocol, Any


class LongTermMemoryStore(Protocol):
    def read(self, key: str) -> Any: ...
    def write(self, key: str, value: Any): ...


class InMemoryLongTermMemory:
    """
    Placeholder for DB / Feature Store / Vector DB later.
    """

    def __init__(self):
        self._store = {}

    def read(self, key: str):
        return self._store.get(key)

    def write(self, key: str, value: Any):
        self._store[key] = value

