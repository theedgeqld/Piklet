#http://www.stuffaboutcode.com/2014/06/raspberry-pi-adxl345-accelerometer.html
#http://www.dx.com/p/gy-291-adxl345-digital-3-axis-acceleration-of-gravity-tilt-module-for-arduino-148921#.V4YNz2h96f4

from drivers.adxl345 import ADXL345
from model.sensor import Sensor

class accelerometer(Sensor):
    def __init__(self, scratch, *args, **kwargs):
        Sensor.__init__(self, scratch, *args, **kwargs)
        self.scratch = scratch

        self.accelerometer = ADXL345()

        print("Enabling Accelerometer")

    def tick(self):
        axes = self.accelerometer.getAxes(True)
        self.scratch.updateSensor("accelerometer-x", axes['x'])
        self.scratch.updateSensor("accelerometer-y", axes['y'])
        self.scratch.updateSensor("accelerometer-z", axes['z'])
        self.scratch.broadcast("accelerometer-updated")