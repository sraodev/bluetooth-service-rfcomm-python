"""Storage abstractions for persisting deserialized payloads."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .interfaces import DataSink, DataSource


class JsonFileSink(DataSink):
    """
    Persist objects as JSON into a file.

    Keeps I/O concerns isolated from transport code (Single Responsibility).
    """

    def __init__(self, target_path: str) -> None:
        self._path = Path(target_path)

    def persist(self, obj: Any) -> None:
        serializable = obj if isinstance(obj, Mapping) else {"data": obj}
        with self._path.open("w", encoding="utf-8") as json_file:
            json.dump(serializable, json_file, indent=4)


class JsonFileSource(DataSource):
    """Load JSON content from disk for transmission."""

    def __init__(self, source_path: str) -> None:
        self._path = Path(source_path)

    def load(self) -> Any:
        with self._path.open("r", encoding="utf-8") as json_file:
            return json.load(json_file)

