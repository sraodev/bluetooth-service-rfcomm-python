# Message Schema (placeholder)

Centralize serialization formats here (JSON Schema, Protocol Buffers, Avro,
etc.). All SDKs, microservices, and examples should reference these schemas for
consistent payloads.

Recommended structure:

- `/json/` for JSON Schema files.
- `/proto/` for `.proto` definitions shared with gRPC services.
- `/avro/` or others as needed.

