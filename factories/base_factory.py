"""Abstract base classes for factories."""
from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseFactory(ABC):
    """Abstract base factory class."""

    @abstractmethod
    def create(self, config: Dict[str, Any]) -> Any:
        """
        Create an instance based on configuration.

        Args:
            config: Configuration dictionary

        Returns:
            Created instance
        """
        pass