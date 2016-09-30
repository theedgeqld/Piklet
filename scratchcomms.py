import sys
from array import array
import socket
from event.eventhandler import EventHandler

class ScratchComms:
    def __init__(self, host, port=42001):
        self.socket = None
        self.address = (host, port)

        self.variables = {}

        EventHandler.addListener("packet-received", self.packetReceieved)

    def connect(self):
        """
        When called, it connects to Scratch
        :return:
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(self.address)
            self.socket.setblocking(False)
            return True
        except:
            return False

    def getPacketLengthBytes(self, packet):
        """
        Generates a packet header with the packet length
        :param packet:
        :return: 4 Bytes of the packet length as a header
        """
        if sys.version[0] == "2":
            n = len(packet)
            a = array('c')
            a.append(chr((n >> 24) & 0xFF))
            a.append(chr((n >> 16) & 0xFF))
            a.append(chr((n >> 8) & 0xFF))
            a.append(chr(n & 0xFF))
            return a.tostring()
        elif sys.version[0] == "3":
            return (len(packet)).to_bytes(4, byteorder='big')
        else:
            return None


    def sendScratchCommand(self, command):
        """
        Packs a packet with the header byte and string command provided
        :param command: Valid scratch string command
        :return:
        """
        try:
            if sys.version[0] == "2":
                self.socket.send(self.getPacketLengthBytes(command) + command)
            elif sys.version[0] == "3":
                self.socket.send(self.getPacketLengthBytes(command) + command.encode('utf-8'))
        except ConnectionResetError:
            self.disconnect()


    def broadcast(self, msg):
        EventHandler.callEvent("broadcast", msg)
        self.sendScratchCommand('broadcast {}'.format(msg))

    def updateSensor(self, sensor, value):
        EventHandler.callEvent("sensor-update", (sensor, value))
        self.sendScratchCommand('sensor-update {} {}'.format(sensor, value))

    def packetReceieved(self, data):
        packet = data[4:].decode("utf-8").replace("'", "").strip().split(" ")
        command = packet[0]

        if command == "sensor-update":
            del packet[0]

            """
            Format from scratch is typically:
            sensor-update <key> <value>

            However, when first connecting scratch decides to send...
            sensor-update <key1> <value1> <key2> <value2> ...

            Hence the while loop which keeps iterating over the arguments until it
            has sorted through all the key-value pairs.
            """

            while len(packet) >= 2:
                key, value = packet[0], packet[1]

                try:
                    key = eval(key)
                    self.variables[key] = value
                    EventHandler.callEvent("variable-updated", (key, value))
                except:
                    print(key, value)
                    print(packet)
                    continue

                del packet[0]
                del packet[0]

        elif command == "broadcast":
            value = eval(packet[1])
            EventHandler.callEvent("broadcast-received", value)

    def tick(self):
        rx = None
        try:
            rx = self.socket.recv(1024)
            if rx == b'':
                self.disconnect()
        except:
            pass
        if rx:
            EventHandler.callEvent("packet-received", rx)

    def disconnect(self):
        self.socket.close()
        self.socket = None
        print("Disconnected")
        EventHandler.callEvent("scratch-disconnect", None)