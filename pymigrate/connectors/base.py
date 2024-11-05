from abc import ABC, abstractmethod
from typing import Any, List, Tuple, Dict

class BaseConnector(ABC):
    def __init__(self):
        self._query_count = 0
        self._operations_count = 0

    @abstractmethod
    def connect(self) -> None:
        """Establish database connection."""
        pass

    @abstractmethod
    def execute(self, operation: str, params: Any = None) -> Any:
        """Execute a single operation."""
        pass

    @abstractmethod
    def execute_batch(self, operations: List[Tuple[str, Any]]) -> None:
        """Execute multiple operations in a batch."""
        pass

    @abstractmethod
    def close(self) -> None:
        """Close database connection."""
        pass

    def get_metrics(self) -> Dict[str, int]:
        """Get operation execution metrics."""
        return {
            'query_count': self._query_count,
            'operations_count': self._operations_count
        }

    def reset_metrics(self) -> None:
        """Reset operation metrics."""
        self._query_count = 0
        self._operations_count = 0
