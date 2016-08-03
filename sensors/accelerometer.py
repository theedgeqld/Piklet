#http://www.stuffaboutcode.com/2014/06/raspberry-pi-adxl345-accelerometer.html
#http://www.dx.com/p/gy-291-adxl345-digital-3-axis-acceleration-of-gravity-tilt-module-for-arduino-148921#.V4YNz2h96f4

from drivers.adxl345 import ADXL345
from model.sensor import Sensor

class accelerometer(Sensor):
    def __init__(self, scratch, *args, **kwargs):
        Sensor.__init__(self, scratch, *args, **kwargs)
        self.scratch = scratch

        #External driver located under drivers/adxl345.py
        self.accelerometer = ADXL345()

        print("Enabling Accelerometer")

        self.lastValueX = 0
        self.lastValueY = 0
        self.lastValueZ = 0

        self.threshold = 0.01

    def setRegister(self, key, value):
        if key == "threshold":
            self.threshold = eval(value)

    def tick(self):
        """
        Called regularly. If the accelerometer has a new value
        and that new value is beyond the change threshold, it sends
         it to scratch.
        :return:
        """

        axes = self.accelerometer.getAxes(True)

        if abs(axes['x']-self.lastValueX) > self.threshold:
            self.scratch.updateSensor("accelerometer-x", axes['x'])
            self.lastValueX = axes['x']

        elif abs(axes['y'] - self.lastValueY) > self.threshold:
            self.scratch.updateSensor("accelerometer-y", axes['y'])
            self.lastValueY = axes['y']

        elif abs(axes['z'] - self.lastValueZ) > self.threshold:
            self.scratch.updateSensor("accelerometer-z", axes['z'])
            self.lastValueZ = axes['z']
        self.scratch.broadcast("accelerometer-updated")