from model.sensor import Sensor
import smbus

class sound(Sensor):
    def __init__(self, scratch, *args, **kwargs):
        Sensor.__init__(self, scratch, *args, **kwargs)
        self.bus = smbus.SMBus(1)

        # This is the address we setup in the PCF8591
        self.address = 0x48

        if self.data.lower() == "a1":
            self.adcRegister = 0x40
        elif self.data.lower() == "a2":
            self.adcRegister = 0x41
        elif self.data.lower() == "a3":
            self.adcRegister = 0x42

        self.threshold = 3

        self.lastValue = 0

    def tick(self):
        volume = self.getSoundLevel()

        if abs(volume-self.lastValue) > self.threshold:
            self.scratch.updateSensor("sound", volume)
            self.scratch.broadcast("sound-updated")
            self.lastValue = volume

    def setRegister(self, key, value):
        if self.key == "threshold":
            self.threshold = eval(value)

    def getSoundLevel(self):
        self.bus.write_byte(self.address, self.adcRegister)
        self.bus.read_byte(self.address)  # dummy read to start conversion
        volume = self.bus.read_byte(self.address)