# Python SDK

This folder contains the production-ready Python implementation of the Universal
Bluetooth SDK. Highlights:

- `bluetooth_service/`: reusable package with server/client orchestration,
  serializers, storage adapters, and socket facades.
- `run_server.py`, `run_client.py`: batteries-included entry points that consume
  the SDK.
- `scripts/install_dependencies.sh`: helper to install PyBluez and system
  requirements on Debian/Ubuntu hosts.
- `tests/`: pytest suite with transport stubs to validate protocol behavior.

## Quick start

```bash
sudo ./scripts/install_dependencies.sh
python3 run_server.py      # Raspberry Pi / receiver
python3 run_client.py      # sender
```

Run from within `sdk/python` or adjust your `PYTHONPATH` if launching elsewhere.

## Tests

```bash
python3 -m pip install pytest
pytest tests/
```

## Customization

- Update `bluetooth_service/config.py` (`ServerSettings`) for server behavior.
- Update `bluetooth_service/client_config.py` (`ClientSettings`) for discovery,
  retries, and payload source.
- Swap serializers/sinks/sources by injecting your own implementations when
  constructing `BluetoothServer` / `BluetoothClient`.

