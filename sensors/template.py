from model.sensor import Sensor

import random

class template(Sensor):
    def __init__(self, scratch, data=None):
        self.scratch = scratch
        self.data = data

        self.randomNumbers = True

    def start(self):
        print("Template Sensor starting...")

    def stop(self):
        print("Template Sensor stopping...")

    def setRegister(self, key, value):
        print("Register changed", key, value)

        if key == "random":
            if value == "1":
                self.randomNumbers = True
            else:
                self.randomNumbers = False

        if key == "raiseerror":
            if value == "1":
                raise Exception

    def tick(self):
        if self.randomNumbers:
            number = random.randint(0, 10)
        else:
            number = self.data

        self.scratch.updateSensor("template-sensor", number)
        self.scratch.broadcast("template-updated")