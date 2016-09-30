import os

class Servo:
    def __init__(self, pin):
        self.pin = pin
        self.pulse("50%")

    def set(self, pos):
        command = "echo {}={} > /dev/servoblaster".format(self.pin, pos)
        print(command)
        os.system(command)