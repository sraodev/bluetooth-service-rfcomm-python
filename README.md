# Universal Bluetooth SDK

Cross-language, multi-service toolkit for building Bluetooth solutions (RFCOMM
today, BLE-ready tomorrow). The Python SDK is production-ready; other folders
are scaffolding for future Go/Rust SDKs, microservices, and CLI tooling.

## Repository layout

```
.
├── sdk/
│   ├── python/          # fully implemented PyBluez SDK
│   ├── go/              # placeholder for Go SDK
│   └── rust/            # placeholder for Rust SDK
├── microservices/
│   ├── grpc-server/     # future gRPC control-plane
│   └── rest-server/     # future REST façade
├── cli/
│   └── ubtctl/          # future CLI tool
├── examples/            # scenario-specific samples
├── common/              # shared protocols & schemas
└── docs/                # architecture & guides
```

## Python SDK (sdk/python)

### Prerequisites

PyBluez + BlueZ on Linux (tested on Raspberry Pi OS / Ubuntu). Install via the
helper script:

```bash
cd sdk/python
sudo ./scripts/install_dependencies.sh
```

Or install packages manually (Debian/Ubuntu):

```
sudo apt-get install python3 python3-dev python3-pip ipython3
sudo apt-get install bluetooth libbluetooth-dev bluez bluez-tools blueman
sudo python3 -m pip install pybluez
```

### Usage

Run commands from `sdk/python` (or set `PYTHONPATH` accordingly).

1. **Start the server (e.g., on Raspberry Pi)**
   ```bash
   cd sdk/python
   sudo python3 run_server.py
   ```
   - Customize behaviour via `bluetooth_service/config.py` (`ServerSettings`).
   - Use `LOG_CFG=/path/to/logger.json` to override the default logger config.

2. **Send data from the client**
   ```bash
    cd sdk/python
    sudo python3 run_client.py
   ```
   - Update `bluetooth_service/client_config.py` for UUID, discovery retries,
     payload source, etc.
   - Default payload is `text.json`; inject your own `DataSource` for custom
     payloads.

3. **Run unit tests (no Bluetooth hardware required)**
   ```bash
   cd sdk/python
   python3 -m pip install pytest
   pytest tests/
   ```
   Tests use socket stubs to stay deterministic on any host.

## Platform setup tips

Make your Raspberry Pi discoverable:

```
sudo hciconfig hci0 piscan
```

Run the classic inquiry example (optional):

```
sudo python inquiry.py
```

## Known Issues

```
Traceback (most recent call last):
  File "/usr/share/doc/python-bluez/examples/simple/rfcomm-server.py", line 20, in <module>
    profiles = [ SERIAL_PORT_PROFILE ],
  File "/usr/lib/python2.7/dist-packages/bluetooth/bluez.py", line 176, in advertise_service
    raise BluetoothError (str (e))
bluetooth.btcommon.BluetoothError: (2, 'No such file or directory')
```

## Possible fixes

Make sure you are using sudo when running the python script
Make sure you have the serial profile loaded. How to enable the serial profile.

As it turns out, the culprit is bluetoothd, the Bluetooth daemon. Using SDP with bluetoothd requires deprecated features for some silly reason, so to fix this, the daemon must be started in compatibility mode with bluetoothd -C (or bluetooth --compat).

You need to run the Bluetooth daemon in 'compatibility' mode. Edit /lib/systemd/system/bluetooth.service and add '-C' after 'bluetoothd'. Reboot.

```
sudo sdptool add SP
```

Or

Find location of bluetooth.service by:

```
systemctl status bluetooth.service
```
Then edit bluetooth.service and look for ExecStart=/usr/libexec/bluetooth/bluetoothd
Append --compat at the end of this line, save, and then run

```
service bluetooth start
```

If all goes well, you should be able to successfully run

```
sudo sdptool browse local
```

Finally, reset the adapter:

```
sudo hciconfig -a hci0 reset
```

## Roadmap

- Flesh out Go/Rust SDKs under `sdk/`.
- Build microservices (gRPC + REST) that wrap the SDK for remote control.
- Ship `ubtctl` CLI for device management.
- Provide ready-to-run examples (chat, sensor stream, file transfer).

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**. Please read the [contribution guidelines](https://github.com/sraodev/super-opensource-cheat-sheets/blob/master/contributing.md) first.

## Reference

[Bluetooth Programming with Python 3](http://blog.kevindoran.co/bluetooth-programming-with-python-3)

[Bluetooth programming with Python - PyBluez](https://people.csail.mit.edu/albert/bluez-intro/x232.html)

[Bluetooth for Programmers](http://people.csail.mit.edu/rudolph/Teaching/Articles/PartOfBTBook.pdf)

[Bluetooth Python extension module](https://github.com/karulis/pybluez)
