#!/usr/bin/python

"""
Entry point for the refactored RFCOMM Bluetooth client SDK.
"""

from bluetooth_service.client_config import ClientSettings
from bluetooth_service.client_sdk import bootstrap_and_send


def main() -> None:
    settings = ClientSettings()
    bootstrap_and_send(settings)


if __name__ == "__main__":
    main()

