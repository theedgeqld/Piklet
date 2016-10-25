from model.sensor import Sensor
from drivers.hcsr04 import HCSR04
from drivers.piklet import Piklet

class ultrasonic(Sensor):
    def __init__(self, scratch, *args, **kwargs):
        Sensor.__init__(self, scratch, *args, **kwargs)
        self.pins = Piklet.pins[self.data]

    def start(self):
        self.ultrasonic = HCSR04()

    def stop(self):
        pass

    def tick(self):
        print("tick")
        distance = self.ultrasonic.get()

        self.scratch.updateSensor("ultrasonic", distance)
        self.scratch.broadcast("ultrasonic-updated")
