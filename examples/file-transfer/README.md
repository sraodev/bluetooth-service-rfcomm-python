# File Transfer Example (placeholder)

Goal: reliably transfer binary files (images, firmware, etc.) using the SDK.

Ideas:

- Chunk files, send with sequence numbers, resume on failure.
- Verify integrity with hashes defined in `common/protocol/`.
- Showcase integration with the CLI (`ubtctl file send ...`).

