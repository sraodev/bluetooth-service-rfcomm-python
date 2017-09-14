# Bluetooth Services (PyBluez) with RFCOMM sockets

This application connects two devices over Bluetooth and allows one to send messages to the other using json. The sending device runs belClient.py, and the receiving device runs bleServer.py

## Getting Started

How to setup a bluetooth server in a Raspberry Pi so an Linux can connect to it.

### Pre-quisites

This python-script uses Bluez, Linux's Bluetooth protocol stack, we'll be using PyBluez, a Python API for accessing the bluetooth resources using the bluez protocol.

### Installation

```
sudo apt-get install python-pip python-dev ipython

sudo apt-get install bluetooth libbluetooth-dev

sudo apt-get install bluez-utils blueman

sudo apt-get install bluez python-bluez

sudo pip install pybluez`
```

You've installed the Python 2 version of the bluez bindings. Either run the script using python2 or install the Python 3 bindings. Since they aren't packaged, you would need to install them using pip:

```
sudo python3 -m pip install pybluez`
```

### Setup your Raspberry Pi

#### Make your device discoverable
```
sudo hciconfig hci0 piscan
```

#### Scanning for devices run the inquiry example:
```
sudo python inquiry.py
```

#### Running the Bluetooth Server on RaspberryPi:
```
sudo python bleServer.py
```

#### Running the Bluetooth Client on Linux box:
```
sudo python bleClient.py
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

## Reference

[Bluetooth Programming with Python 3](http://blog.kevindoran.co/bluetooth-programming-with-python-3)

[Bluetooth programming with Python - PyBluez](https://people.csail.mit.edu/albert/bluez-intro/x232.html)

[Bluetooth for Programmers](http://people.csail.mit.edu/rudolph/Teaching/Articles/PartOfBTBook.pdf)

[Bluetooth Python extension module](https://github.com/karulis/pybluez)
