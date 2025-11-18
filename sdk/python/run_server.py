#!/usr/bin/python

"""
Entry point for the refactored RFCOMM Bluetooth server SDK.
"""

from bluetooth_service.config import ServerSettings
from bluetooth_service.sdk import bootstrap_and_run


def main() -> None:
    settings = ServerSettings()
    bootstrap_and_run(settings)


if __name__ == "__main__":
    main()

