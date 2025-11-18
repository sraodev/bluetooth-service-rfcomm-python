"""Custom exceptions for the Bluetooth server SDK."""

from __future__ import annotations

from typing import Optional


class BluetoothServerError(RuntimeError):
    """Domain specific exception raised by the SDK."""

    def __init__(self, message: str, *, cause: Optional[BaseException] = None) -> None:
        super().__init__(message)
        self.__cause__ = cause

