from model.sensor import Sensor
from drivers.lb1930mc import LB1930MC
from drivers.piklet import Piklet

class motor(Sensor):
    def __init__(self, scratch, *args, **kwargs):
        Sensor.__init__(self, scratch, *args, **kwargs)

    def start(self):
        pins = None
        if "," in self.data:
            pins = self.data.split(",")
            pins = (int(pins[0]), int(pins[1]))
        else:
            pins = Piklet.pins["M"+self.data]

        self.motorDriver = LB1930MC(pins)

    def stop(self):
        self.motorDriver.stop()

    def setRegister(self, key, value):
        if key == "speed":
            self.motorDriver.set(int(value))

    def tick(self):
        pass