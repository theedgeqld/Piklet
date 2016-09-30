from model.sensor import Sensor
from drivers.lb1930mc import LB1930MC

class motor(Sensor):
    def __init__(self, scratch, *args, **kwargs):
        Sensor.__init__(self, scratch, *args, **kwargs)

    def start(self):
        self.motorDriver = LB1930MC(motor=self.data)

    def stop(self):
        self.motorDriver.stop()

    def setRegister(self, key, value):
        if key == "speed":
            self.motorDriver.set(int(value))

    def tick(self):
        pass