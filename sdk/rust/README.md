# Rust SDK (placeholder)

This directory is reserved for a future Rust implementation of the Universal
Bluetooth SDK.

Ideas for contributors:

- Expose async-friendly client/server wrappers on top of BlueZ/WinRT APIs.
- Keep the protocol definitions shared with other languages via
  `common/message-schema/`.
- Provide FFI hooks so the microservices and CLI can reuse the Rust core.

Interested? Open an issue to coordinate the initial design.

