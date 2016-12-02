import serial, time
from model.sensor import ThreadedSensor

class RFID(ThreadedSensor):
    pinGroup = "serial"

    COMMAND_WAKE = b'\x55\x55\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x03\xfd\xd4\x14\x01\x17\x00'
    COMMAND_READ = b'\x00\x00\xff\x04\xfc\xd4\x4a\x01\x00\xe1\x00'

    def __init__(self, scratch, *args, **kwargs):
        ThreadedSensor.__init__(self, scratch, *args, **kwargs)

        self.serial = serial.Serial('/dev/ttyAMA0', 115200)
        self.lastCheckTime = 0
        self.lastTag = ""

    def start(self):
        self.wakeRFID()
        ThreadedSensor.start(self)

    def stop(self):
        self.serial.close()
        ThreadedSensor.stop(self)

    def loop(self):
        time.sleep(0.1)
        while self.running:
            #Get's the RFID tag from the sensor. This command waits until a card is presented
            id = self.readRFID()

            #If it's been longer than 1 second since it last sent a message to scratch...
            if time.time() - self.lastCheckTime > 1 or self.lastTag != id:
                self.lastTag = id

                self.scratch.updateSensor("rfid", id)
                self.scratch.broadcast("rfid-updated")

                self.lastCheckTime = time.time()

    def wakeRFID(self):
        self.serial.write(RFID.COMMAND_WAKE)

    def readRFID(self):
        self.serial.flush()
        self.serial.write(RFID.COMMAND_READ)
        self.serial.flushInput()
        rx = self.serial.read(25)
        id = "".join(list([str(x) for x in rx]))
        return id