from typing import Dict, Any


class DecisionContext:
    """
    Immutable decision context passed across patterns.

    Prevents hidden state and ambiguity.
    """

    def __init__(self, data: Dict[str, Any]):
        self._data = dict(data)

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def extend(self, updates: Dict[str, Any]) -> "DecisionContext":
        merged = dict(self._data)
        merged.update(updates)
        return DecisionContext(merged)

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._data)

