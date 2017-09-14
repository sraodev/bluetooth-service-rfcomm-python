#!/usr/bin/python

# File: bleClient.py
# Auth: P Srinivas Rao
# Desc: Bluetooth client application that uses RFCOMM sockets
#       intended for use with rfcomm-server
import os
import sys
import time
import logging
import logging.config
import json #Uses JSON package
import cPickle as pickle #Serializing and de-serializing a Python object structure
from bluetooth import * #Python Bluetooth library

logger = logging.getLogger('bleClientLogger')

def startLogging(
    default_path='configLogger.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    #Setup logging configuration
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

class bleClient:
    def __init__(self, clientSocket=None):
        if clientSocket is None:
            self.clientSocket = clientSocket
            self.bleService = None
            self.addr = None
            self.uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
            self.jsonFile ="text.json"
            self.jsonObj = None
        else:
            self.clientSocket = clientSocket

    def getBluetoothServices(self):
        try:
            logger.info("Searching for  Bluetooth services ...")
            for reConnect in range(2, 4):
                bleService = find_service( uuid = self.uuid, address = self.addr )
                if len(bleService) == 0:
                    logger.info("Re-connecting  Bluetooth services : %d attempt", reConnect)
                else:
                    break
            if not bleService: raise SystemExit(), KeyboardInterrupt()
            else:
                logger.info("Found  Bluetooth services ..")
                logger.info("Protocol\t: %s", bleService[0]['protocol'])
                logger.info("Name\t\t: %s", bleService[0]['name'])
                logger.info("Service-id\t: %s", bleService[0]['service-id'])
                logger.info("Profiles\t: %s", bleService[0]['profiles'])
                logger.info("Service-class\t: %s", bleService[0]['service-classes'])
                logger.info("Host\t\t: %s", bleService[0]['host'])
                logger.info("Provider\t: %s", bleService[0]['provider'])
                logger.info("Port\t\t: %s", bleService[0]['port'])
                logger.info("Description\t: %s", bleService[0]['description'])
                self.bleService = bleService
        except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
            logger.error("Couldn't find the RaspberryPi Bluetooth service : Invalid uuid", exc_info=True)

    def getBluetoothSocket(self):
        try:
            self.clientSocket=BluetoothSocket( RFCOMM )
            logger.info("Bluetooth client socket successfully created for RFCOMM service  ...")
        except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
            logger.error("Failed to create the bluetooth client socket for RFCOMM service  ...  ", exc_info=True)

    def getBluetoothConnection(self):
        try:
            bleServiceInfo = self.bleService[0]
            logger.info("Connecting to \"%s\" on %s with port %s" % (bleServiceInfo['name'], bleServiceInfo['host'], bleServiceInfo['port']))
            self.clientSocket.connect((bleServiceInfo['host'], bleServiceInfo['port']))
            logger.info("Connected successfully to %s "% (bleServiceInfo['name']))
        except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
            logger.error("Failed to connect to \"%s\" on address %s with port %s" % (bleServiceInfo['name'], bleServiceInfo['host'], bleServiceInfo['port']), exc_info=True)

    def readJsonFile(self):
        try:
            jsonFileObj = open(self.lsonFile,"r")
            logger.info("File successfully uploaded to %s" % (jsonFileObj))
            self.jsonObj = json.load(jsonFileObj)
            logger.info("Content loaded successfully from the %s file" %(self.jsonFile))
            jsonFileObj.close()
        except (Exception, IOError) as e:
            logger.error("Failed to load content from the %s" % (self.jsonFile), exc_info=True)

    def serializeData(self):
        try:
            serializedData = pickle.dumps(self.jsonObj)
            logger.info("Object successfully converted to a serialized string")
            return serializedData
        except (Exception, pickle.PicklingError) as e:
            logger.error("Failed to convert json object  to serialized string", exc_info=True)

    def sendData(self, _serializedData):
        try:
            logger.info("Sending data over bluetooth connection")
            _serializedData =str(len(_serializedData))+ ":"+_serializedData
            self.clientSocket.send(_serializedData)
            time.sleep(0.5)
            while True:
                dataRecv= self.clientSocket.recv(1024)
                if dataRecv in ['EmptyBufferResend', 'CorruptedBufferResend', 'DelimiterMissingBufferResend']:
                    self.clientSocket.send(_serializedData)
                    time.sleep(0.5)
                    logger.info("%s : Re-sending data over bluetooth connection" %(dataRecv))
                else:
                    break
            logger.info("Data sent successfully over bluetooth connection")
        except (Exception, IOError) as e:
            logger.error("Failed to send data over bluetooth connection", exc_info=True)

    def closeBluetoothSocket(self):
        try:
            self.clientSocket.close()
            logger.info("Bluetooth client socket successfully closed ...")
        except (Exception, BluetoothError, SystemExit, KeyboardInterrupt) as e:
            logger.error("Failed to close the bluetooth client socket ", exc_info=True)

    def start(self):
        # Search for the RaspberryPi Bluetooth service
        self.getBluetoothServices()
        # Create the client socket
        self.getBluetoothSocket()
        # Connect to bluetooth service
        self.getBluetoothConnection()

    def send(self):
        # Load the contents from the file, which creates a new json object
        self.readJsonFile()
        # Convert the json object to a serialized string
        serializedData = self.serializeData()
        # Sending data over bluetooth connection
        self.sendData(serializedData)

    def stop(self):
        # Disconnecting bluetooth service
        self.closeBluetoothSocket()

if __name__ == '__main__':
    startLogging()
    logger.info("Setup logging configuration")
    bleClnt = bleClient()
    bleClnt.start()
    bleClnt.send()
    bleClnt.stop()
