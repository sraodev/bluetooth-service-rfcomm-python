"""Concrete serializer/deserializer implementations."""

from __future__ import annotations

import pickle
from typing import Any

from .interfaces import Deserializer, Serializer


class PickleDeserializer(Deserializer):
    """Deserializer that uses Python's pickle module (Strategy implementation)."""

    def deserialize(self, payload: bytes) -> Any:
        return pickle.loads(payload)


class PickleSerializer(Serializer):
    """Serializer counterpart used by the client."""

    def serialize(self, obj: Any) -> bytes:
        return pickle.dumps(obj)

