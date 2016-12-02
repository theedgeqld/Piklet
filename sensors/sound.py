from model.sensor import Sensor
import smbus
from drivers.mcp3208 import MCP3208
from drivers.piklet import Piklet
from util.runningaverage import RunningAverage

class sound(Sensor):
    pinGroup = "analog"

    def __init__(self, scratch, *args, **kwargs):
        Sensor.__init__(self, scratch, *args, **kwargs)

        self.adcChannel = Piklet.pins["SOUND"]
        self.adc = MCP3208()

        self.average = RunningAverage(20)

        self.threshold = 1
        self.lastValue = 0

    def tick(self):
        volume = self.getSoundLevel()
        self.average.add(volume)
        self.deviation = volume - self.average.getAverage()

        if not volume:
            volume = 0

        if abs(self.deviation) > self.threshold:
            self.scratch.updateSensor("sound", volume)
            self.scratch.broadcast("sound-updated")
            self.lastValue = volume

    def setRegister(self, key, value):
        print("Set register {} to {}".format(key, value))
        print(key)
        if key == "threshold":
            print("Thresholding...")
            self.threshold = int(value)
            print("Set sound sensor threshold to {}".format(self.threshold))

    def getSoundLevel(self):
        return self.adc.getValue(self.adcChannel)