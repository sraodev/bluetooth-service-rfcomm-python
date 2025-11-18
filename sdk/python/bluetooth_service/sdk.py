"""Public SDK surface for consumers that want batteries included."""

from __future__ import annotations

import logging
from typing import Any, Optional

from .config import ServerSettings
from .logging_utils import configure_logging
from .serializers import PickleDeserializer
from .server import BluetoothServer
from .storage import JsonFileSink

logger = logging.getLogger(__name__)


class BluetoothServerSDK:
    """
    Facade that wires together the default stack.

    Provides a simple `run_once()` helper while leaving hooks for dependency
    injection when consumers need more control.
    """

    def __init__(self, server: BluetoothServer) -> None:
        self._server = server

    @classmethod
    def default(
        cls,
        settings: Optional[ServerSettings] = None,
    ) -> "BluetoothServerSDK":
        settings = settings or ServerSettings()
        server = BluetoothServer(
            settings,
            deserializer=PickleDeserializer(),
            sink=JsonFileSink(settings.json_file),
        )
        return cls(server)

    def run_once(self) -> Any:
        """
        Start the server, receive one payload, persist it, and stop.

        Shields callers from lifecycle handling (Template Method).
        """
        logger.debug("Starting SDK run loop")
        try:
            self._server.start()
            return self._server.receive_once()
        finally:
            self._server.stop()


def bootstrap_and_run(settings: Optional[ServerSettings] = None) -> Any:
    """
    Convenience helper that also configures logging from settings.
    """

    settings = settings or ServerSettings()
    configure_logging(settings.logging_config_path, env_key=settings.log_env_key)
    sdk = BluetoothServerSDK.default(settings)
    return sdk.run_once()

