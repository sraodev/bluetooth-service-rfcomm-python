#!/usr/bin/python

# File: bleServer.py
# Auth: P Srinivas Rao
# Desc: Bluetooth server application that uses RFCOMM sockets

import os
import sys
import time
import logging
import logging.config
import json # Uses JSON package
import cPickle as pickle # Serializing and de-serializing a Python object structure
from bluetooth import * # Python Bluetooth library

logger = logging.getLogger('bleServerLogger')

def startLogging(
    default_path='configLogger.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    # Setup logging configuration
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

class bleServer:
    def __init__(self, serverSocket=None, clientSocket=None):
        if serverSocket is None:
            self.dataObj = None
            self.serverSocket = serverSocket
            self.clientSocket = clientSocket
            self.serviceName="BluetoothServices"
            self.jsonFile ="text.json"
            self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        else:
            self.serverSocket = serverSocket
            self.clientSocket = clientSocket

    def getBluetoothSocket(self):
        try:
            self.serverSocket=BluetoothSocket( RFCOMM )
            logger.info("Bluetooth server socket successfully created for RFCOMM service...")
        except (BluetoothError, SystemExit, KeyboardInterrupt) as e:
            logger.error("Failed to create the bluetooth server socket ", exc_info=True)

    def getBluetoothConnection(self):
        try:
            self.serverSocket.bind(("",PORT_ANY))
            logger.info("Bluetooth server socket bind successfully on host "" to PORT_ANY...")
        except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
            logger.error("Failed to bind server socket on host to PORT_ANY ... ", exc_info=True)
        try:
            self.serverSocket.listen(1)
            logger.info("Bluetooth server socket put to listening mode successfully ...")
        except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
            logger.error("Failed to put server socket to listening mode  ... ", exc_info=True)
        try:
            port=self.serverSocket.getsockname()[1]
            logger.info("Waiting for connection on RFCOMM channel %d" % (port))
        except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
            logger.error("Failed to get connection on RFCOMM channel  ... ", exc_info=True)

    def advertiseBluetoothService(self):
        try:
            advertise_service( self.serverSocket, self.serviceName,
                            service_id = self.uuid,
                            service_classes = [ self.uuid, SERIAL_PORT_CLASS ],
                            profiles = [ SERIAL_PORT_PROFILE ],
        #                   protocols = [ OBEX_UUID ]
                            )
            logger.info("%s advertised successfully ..." % (self.serviceName))
        except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
            logger.error("Failed to advertise bluetooth services  ... ", exc_info=True)

    def acceptBluetoothConnection(self):
        try:
            self.clientSocket, clientInfo = self.serverSocket.accept()
            logger.info("Accepted bluetooth connection from %s", clientInfo)
        except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
            logger.error("Failed to accept bluetooth connection ... ", exc_info=True)

    def recvData(self):
        try:
            while True:
                data= self.clientSocket.recv(1024)
                if not data:
                    self.clientSocket.send("EmptyBufferResend")
                # remove the length bytes from the front of buffer
                # leave any remaining bytes in the buffer!
                dataSizeStr, ignored, data = data.partition(':')
                dataSize = int(dataSizeStr)
                if len(data) < dataSize:
                    self.clientSocket.send("CorruptedBufferResend")
                else:
                    self.clientSocket.send("DataRecived")
                    break
            logger.info("Data received successfully over bluetooth connection")
            return data
        except (Exception, IOError, BluetoothError) as e:
            pass

    def deserializedData(self, _dataRecv):
        try:
            self.dataObj=pickle.loads(_dataRecv)
            logger.info("Serialized string converted successfully to object")
        except (Exception, pickle.UnpicklingError) as e:
            logger.error("Failed to de-serialized string ... ", exc_info=True)

    def writeJsonFile(self):
        try:
            # Open a file for writing
            jsonFileObj = open(self.jsonFile,"w")
            logger.info("%s file successfully opened to %s" % (self.jsonFile, jsonFileObj))
            # Save the dictionary into this file
            # (the 'indent=4' is optional, but makes it more readable)
            json.dump(self.dataObj,jsonFileObj, indent=4)
            logger.info("Content dumped successfully to the %s file" %(self.jsonFile))
            # Close the file
            jsonFileObj.close()
            logger.info("%s file successfully closed" %(self.jsonFile))
        except (Exception, IOError) as e:
            logger.error("Failed to write json contents to the file ... ", exc_info=True)

    def closeBluetoothSocket(self):
        try:
            self.clientSocket.close()
            self.serverSocket.close()
            logger.info("Bluetooth sockets successfully closed ...")
        except (Exception, BluetoothError) as e:
            logger.error("Failed to close the bluetooth sockets ", exc_info=True)

    def start(self):
            # Create the server socket
            self.getBluetoothSocket()
            # get bluetooth connection to port # of the first available
            self.getBluetoothConnection()
            # advertising bluetooth services
            self.advertiseBluetoothService()
            # Accepting bluetooth connection
            self.acceptBluetoothConnection()

    def receive(self):
            # receive data
            dataRecv=self.recvData()
            # de-serializing data
            self.deserializedData(dataRecv)
            # Writing json object to the file
            self.writeJsonFile()

    def stop(self):
            # Disconnecting bluetooth sockets
            self.closeBluetoothSocket()

if __name__ == '__main__':
    startLogging()
    bleSvr = bleServer()
    bleSvr.start()
    bleSvr.receive()
    bleSvr.stop()
