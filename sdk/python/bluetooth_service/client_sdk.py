"""Public SDK facade for the Bluetooth client."""

from __future__ import annotations

import logging
from typing import Any, Optional

from .client import BluetoothClient
from .client_config import ClientSettings
from .logging_utils import configure_logging
from .serializers import PickleSerializer
from .storage import JsonFileSource

logger = logging.getLogger(__name__)


class BluetoothClientSDK:
    """Batteries-included client orchestration."""

    def __init__(self, client: BluetoothClient) -> None:
        self._client = client

    @classmethod
    def default(
        cls,
        settings: Optional[ClientSettings] = None,
    ) -> "BluetoothClientSDK":
        settings = settings or ClientSettings()
        client = BluetoothClient(
            settings,
            serializer=PickleSerializer(),
            source=JsonFileSource(settings.json_file),
        )
        return cls(client)

    def run_once(self) -> Any:
        logger.debug("Starting client SDK run loop")
        try:
            self._client.start()
            return self._client.send_once()
        finally:
            self._client.stop()


def bootstrap_and_send(settings: Optional[ClientSettings] = None) -> Any:
    settings = settings or ClientSettings()
    configure_logging(settings.logging_config_path, env_key=settings.log_env_key)
    sdk = BluetoothClientSDK.default(settings)
    return sdk.run_once()

