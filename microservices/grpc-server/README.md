# gRPC Server (placeholder)

This service will expose the Universal Bluetooth SDK over gRPC for remote
control/orchestration.

Suggested next steps:

1. Define protobuf contracts in `common/message-schema/`.
2. Implement adapters that call into the Python/Go/Rust SDK layers.
3. Provide deployment scripts (Docker/systemd/K8s) once the API is stable.

