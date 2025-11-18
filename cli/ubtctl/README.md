# ubtctl CLI (placeholder)

`ubtctl` will become the unified command-line interface for managing Universal
Bluetooth SDK deployments (pairing devices, pushing configs, triggering sends,
etc.).

Proposed features:

- `ubtctl server start/stop/status`
- `ubtctl client send --file text.json`
- `ubtctl discover` to list nearby devices/services

Implementation can build on the Python SDK initially, with later support for Go
or Rust binaries.

