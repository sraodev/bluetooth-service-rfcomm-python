"""Protocol definitions describing extension points for the SDK."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Protocol


class Deserializer(Protocol):
    """Strategy interface (Strategy pattern) for turning bytes into Python objects."""

    def deserialize(self, payload: bytes) -> Any:
        """Convert raw payload into a Python object."""


class DataSink(ABC):
    """Abstraction for persisting Python objects produced by the server."""

    @abstractmethod
    def persist(self, obj: Any) -> None:
        """Persist the given object."""


class Serializer(Protocol):
    """Strategy for turning Python objects into wire-ready bytes."""

    def serialize(self, obj: Any) -> bytes:
        """Convert a Python object into bytes."""


class DataSource(ABC):
    """Abstraction for retrieving Python objects to send to the server."""

    @abstractmethod
    def load(self) -> Any:
        """Load and return the next object to send."""

