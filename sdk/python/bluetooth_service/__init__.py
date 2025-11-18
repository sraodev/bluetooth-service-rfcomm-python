"""
bluetooth_service
=================

SDK-style helpers and abstractions for building RFCOMM Bluetooth clients/servers.
"""

from .client import BluetoothClient
from .client_config import ClientSettings
from .client_sdk import BluetoothClientSDK
from .config import ServerSettings
from .server import BluetoothServer
from .sdk import BluetoothServerSDK

__all__ = [
    "BluetoothClient",
    "BluetoothClientSDK",
    "ClientSettings",
    "BluetoothServer",
    "BluetoothServerSDK",
    "ServerSettings",
]

