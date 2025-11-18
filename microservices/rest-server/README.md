# REST Server (placeholder)

Goal: expose Bluetooth server/client capabilities via RESTful endpoints for easy
integration with web/mobile apps.

Roadmap ideas:

1. Align resource models with `common/message-schema/`.
2. Reuse the gRPC service definitions via gRPC-Gateway or implement a native REST
   controller that talks to the SDK.
3. Document authentication/authorization requirements for remote control of BT
   devices.

