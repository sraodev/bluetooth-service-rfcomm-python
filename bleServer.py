#!/usr/bin/python

# File: bleServer.py
# Auth: P Srinivas Rao
# Desc: Bluetooth server application that uses RFCOMM sockets
import sys
import os
import logging
import logging.config
import json  # Uses JSON package
import pickle  # Serializing and de-serializing a Python object structure
import bluetooth  # Python Bluetooth library

logger = logging.getLogger("bleServerLogger")


def startLogging(
    default_path="configLogger.json", default_level=logging.INFO, env_key="LOG_CFG"
):
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


class bleServer:
    def __init__(self, server_socket=None, client_socket=None):
        if server_socket is None:
            self.data_obj = None
            self.server_socket = server_socket
            self.client_socket = client_socket
            self.service_name = "BluetoothServices"
            self.json_file = "text.json"
            self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        else:
            self.server_socket = server_socket
            self.client_socket = client_socket

    def getBluetoothSocket(self):
        try:
            self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            logger.info(
                "Bluetooth server socket successfully created for RFCOMM service..."
            )
        except (bluetooth.BluetoothError, SystemExit, KeyboardInterrupt) as _:
            logger.error("Failed to create the bluetooth server socket ", exc_info=True)
            return False
        return True

    def getBluetoothConnection(self):
        try:
            self.server_socket.bind(("", bluetooth.PORT_ANY))
            logger.info(
                "Bluetooth server socket bind successfully on host '' to PORT_ANY..."
            )
        except (
            Exception,
            bluetooth.BluetoothError,
            SystemExit,
            KeyboardInterrupt,
        ) as _:
            logger.error(
                "Failed to bind server socket on host to PORT_ANY ... ", exc_info=True
            )
            return False

        try:
            self.server_socket.listen(1)
            logger.info(
                "Bluetooth server socket put to listening mode successfully ..."
            )
        except (
            Exception,
            bluetooth.BluetoothError,
            SystemExit,
            KeyboardInterrupt,
        ) as _:
            logger.error(
                "Failed to put server socket to listening mode  ... ", exc_info=True
            )
            return False
        try:
            port = self.server_socket.getsockname()[1]
            msg = "Waiting for connection on RFCOMM channel %d" % (port)
            logger.info(msg)
        except (
            Exception,
            bluetooth.BluetoothError,
            SystemExit,
            KeyboardInterrupt,
        ) as _:
            logger.error(
                "Failed to get connection on RFCOMM channel  ... ", exc_info=True
            )
            return False

        return True

    def advertiseBluetoothService(self):
        """Advertise BT service"""
        try:
            bluetooth.advertise_service(
                self.server_socket,
                self.service_name,
                service_id=self.uuid,
                service_classes=[self.uuid, bluetooth.SERIAL_PORT_CLASS],
                profiles=[bluetooth.SERIAL_PORT_PROFILE],
                #                   protocols = [ OBEX_UUID ]
            )
            msg = "%s advertised successfully ..." % (self.service_name)
            logger.info(msg)
        except (
            Exception,
            bluetooth.BluetoothError,
            SystemExit,
            KeyboardInterrupt,
        ) as _:
            logger.error("Failed to advertise bluetooth services  ... ", exc_info=True)
            return False

        return True

    def acceptBluetoothConnection(self):
        try:
            self.client_socket, client_info = self.server_socket.accept()
            logger.info("Accepted bluetooth connection from %s", client_info)
        except (
            Exception,
            bluetooth.BluetoothError,
            SystemExit,
            KeyboardInterrupt,
        ) as _:
            logger.error("Failed to accept bluetooth connection ... ", exc_info=True)

    def recvData(self):
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    self.client_socket.send("EmptyBufferResend")
                # remove the length bytes from the front of buffer
                # leave any remaining bytes in the buffer!
                print("Incoming data")
                dataSizeStr, _, data = data.partition(":")
                dataSize = int(dataSizeStr)
                if len(data) < dataSize:
                    self.client_socket.send("CorruptedBufferResend")
                else:
                    self.client_socket.send("DataRecived")
                    break
            logger.info("Data received successfully over bluetooth connection")
            return data
        except (Exception, IOError, bluetooth.BluetoothError) as _:
            pass

    def deserializedData(self, _data_recv):
        try:
            self.data_obj = pickle.loads(_data_recv)
            logger.info("Serialized string converted successfully to object")
        except (Exception, pickle.UnpicklingError) as _:
            logger.error("Failed to de-serialized string ... ", exc_info=True)

    def writeJsonFile(self):
        try:
            # Open a file for writing
            json_file_obj = open(self.json_file, "w", encoding="utf-8")
            msg = "%s file successfully opened to %s" % (self.json_file, json_file_obj)
            logger.info(msg)
            # Save the dictionary into this file
            # (the 'indent=4' is optional, but makes it more readable)
            json.dump(self.data_obj, json_file_obj, indent=4)
            msg = "Content dumped successfully to the %s file" % (self.json_file)
            logger.info(msg)
            # Close the file
            json_file_obj.close()
            msg = "%s file successfully closed" % (self.json_file)
            logger.info(msg)
        except (Exception, IOError) as _:
            logger.error(
                "Failed to write json contents to the file ... ", exc_info=True
            )

    def closeBluetoothSocket(self):
        try:
            self.client_socket.close()
            self.server_socket.close()
            logger.info("Bluetooth sockets successfully closed ...")
        except (Exception, bluetooth.BluetoothError) as _:
            logger.error("Failed to close the bluetooth sockets ", exc_info=True)

    def start(self):
        # Create the server socket
        res = self.getBluetoothSocket()
        if not res:
            sys.exit(0)
        # get bluetooth connection to port # of the first available
        res = self.getBluetoothConnection()
        if not res:
            sys.exit(0)
        # advertising bluetooth services
        res = self.advertiseBluetoothService()
        if not res:
            sys.exit(0)
        # Accepting bluetooth connection
        self.acceptBluetoothConnection()

    def receive(self):
        # receive data
        data_recv = self.recvData()
        # de-serializing data
        self.deserializedData(data_recv)
        # Writing json object to the file
        self.writeJsonFile()

    def stop(self):
        # Disconnecting bluetooth sockets
        self.closeBluetoothSocket()


if __name__ == "__main__":
    startLogging()
    bleSvr = bleServer()
    bleSvr.start()
    bleSvr.receive()
    bleSvr.stop()
