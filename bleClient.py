#!/usr/bin/python

# File: bleClient.py
# Auth: P Srinivas Rao
# Desc: Bluetooth client application that uses RFCOMM sockets
#       intended for use with rfcomm-server
import sys
import os
import time
import logging
import logging.config
import json  # Uses JSON package

# import cPickle as pickle  # Serializing and de-serializing a Python object structure
import pickle

import bluetooth  # Python Bluetooth library

logger = logging.getLogger("bleClientLogger")


def startLogging(
    default_path="configLogger.json", default_level=logging.INFO, env_key="LOG_CFG"
):
    """Init the logging subsystem"""
    # Setup logging configuration
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "rt", encoding="utf-8") as file_handle:
            config = json.load(file_handle)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


class bleClient:
    """Provide Bluetooth Client interface"""

    def __init__(self, client_socket=None):
        if client_socket is None:
            self.client_socket = client_socket
            self.ble_service = None
            self.addr = None
            self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
            self.json_file = "text.json"
            self.json_obj = None
        else:
            self.client_socket = client_socket

    def getBluetoothServices(self):
        """Get BT service"""
        try:
            logger.info("Searching for Bluetooth services ...")
            for reconnect in range(2, 4):
                ble_service = bluetooth.find_service(uuid=self.uuid, address=self.addr)
                if len(ble_service) == 0:
                    logger.info(
                        "Re-connecting Bluetooth services : %d attempt", reconnect
                    )
                else:
                    break
            if not ble_service:
                raise Exception([SystemExit(), KeyboardInterrupt()])
            else:
                logger.info("Found  Bluetooth services ..")
                logger.info("Protocol\t: %s", ble_service[0]["protocol"])
                logger.info("Name\t\t: %s", ble_service[0]["name"])
                logger.info("Service-id\t: %s", ble_service[0]["service-id"])
                logger.info("Profiles\t: %s", ble_service[0]["profiles"])
                logger.info("Service-class\t: %s", ble_service[0]["service-classes"])
                logger.info("Host\t\t: %s", ble_service[0]["host"])
                logger.info("Provider\t: %s", ble_service[0]["provider"])
                logger.info("Port\t\t: %s", ble_service[0]["port"])
                logger.info("Description\t: %s", ble_service[0]["description"])
                self.ble_service = ble_service
        except (
            Exception,
            bluetooth.BluetoothError,
            SystemExit,
            KeyboardInterrupt,
        ) as _:
            logger.error(
                "Couldn't find the RaspberryPi Bluetooth service : Invalid uuid",
                exc_info=True,
            )
            return False

        return True

    def getBluetoothSocket(self):
        """Get the BT socket"""
        try:
            self.client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            logger.info(
                "Bluetooth client socket successfully created for RFCOMM service ... "
            )
        except (
            Exception,
            bluetooth.BluetoothError,
            SystemExit,
            KeyboardInterrupt,
        ) as _:
            logger.error(
                "Failed to create the bluetooth client socket for RFCOMM service ... ",
                exc_info=True,
            )

    def getBluetoothConnection(self):
        """Get the BT connection"""
        ble_service_info = self.ble_service[0]
        msg = (
            f'Connecting to "{ble_service_info["name"]}" on '
            f'{ble_service_info["host"]} with port {ble_service_info["port"]}'
        )
        logger.info(msg)

        attempt = 0
        # Retry a few times
        while True:
            attempt += 1

            try:
                self.client_socket.connect(
                    (ble_service_info["host"], ble_service_info["port"])
                )
                msg = f"Connected successfully to {ble_service_info['name']}"
                logger.info(msg)
                break
            except (
                Exception,
                bluetooth.BluetoothError,
                SystemExit,
                KeyboardInterrupt,
            ) as _:
                msg = (
                    f'Failed to connect to "{ble_service_info["name"]}" on '
                    f'address {ble_service_info["host"]} with port {ble_service_info["port"]}'
                )
                logger.error(
                    msg,
                    exc_info=True,
                )

                time.sleep(1)
                if attempt > 5:
                    return False

        return True

    def readJsonFile(self):
        """Read JSON file"""
        try:
            json_file_obj = open(self.json_file, "r", encoding="utf-8")
            msg = "File successfully uploaded to %s" % (json_file_obj)
            logger.info(msg)
            self.json_obj = json.load(json_file_obj)
            msg = "Content loaded successfully from the %s file" % (self.json_file)
            logger.info(msg)
            json_file_obj.close()
        except (Exception, IOError) as _:
            msg = "Failed to load content from the %s" % (self.json_file)
            logger.error(msg, exc_info=True)

    def serializeData(self):
        """Serialize the data"""
        try:
            serialized_data = pickle.dumps(self.json_obj)
            logger.info("Object successfully converted to a serialized string")
            return serialized_data
        except (Exception, pickle.PicklingError) as _:
            logger.error(
                "Failed to convert json object  to serialized string", exc_info=True
            )

    def sendData(self, serialized_data):
        """Send data via BT"""
        try:
            logger.info("Sending data over bluetooth connection")
            _serialized_data = b""
            _serialized_data += len(serialized_data).to_bytes(2, "little")
            _serialized_data += b":"
            _serialized_data += serialized_data
            self.client_socket.send(_serialized_data)
            time.sleep(0.5)
            while True:
                data_recv = self.client_socket.recv(1024)
                if data_recv in [
                    "EmptyBufferResend",
                    "CorruptedBufferResend",
                    "DelimiterMissingBufferResend",
                ]:
                    self.client_socket.send(_serialized_data)
                    time.sleep(0.5)
                    msg = f"{data_recv} : Re-sending data over bluetooth connection"
                    logger.info(msg)
                else:
                    break
            logger.info("Data sent successfully over bluetooth connection")
        except (Exception, IOError) as _:
            logger.error("Failed to send data over bluetooth connection", exc_info=True)

    def closeBluetoothSocket(self):
        """Close BT socket"""
        try:
            self.client_socket.close()
            logger.info("Bluetooth client socket successfully closed ...")
        except (
            Exception,
            bluetooth.BluetoothError,
            SystemExit,
            KeyboardInterrupt,
        ) as _:
            logger.error("Failed to close the bluetooth client socket ", exc_info=True)

    def start(self):
        """Start the BT interface"""
        # Search for the RaspberryPi Bluetooth service
        res = self.getBluetoothServices()
        if not res:
            logger.error("Failed to get bluetooth services")
            sys.exit(0)
        # Create the client socket
        self.getBluetoothSocket()
        # Connect to bluetooth service
        res = self.getBluetoothConnection()
        if not res:
            logger.error("Failed to get bluetooth connection")
            sys.exit(0)

    def send(self):
        """Send content"""

        # Load the contents from the file, which creates a new json object
        self.readJsonFile()
        # Convert the json object to a serialized string
        serialized_data = self.serializeData()
        # Sending data over bluetooth connection
        self.sendData(serialized_data)

    def stop(self):
        """Stop the BT interface"""

        # Disconnecting bluetooth service
        self.closeBluetoothSocket()


if __name__ == "__main__":
    startLogging()
    logger.info("Setup logging configuration")
    bleClnt = bleClient()
    bleClnt.start()
    bleClnt.send()
    bleClnt.stop()
