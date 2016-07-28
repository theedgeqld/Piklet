from model.sensor import Sensor
import RPi.GPIO as GPIO
import time

class light(Sensor):
    def __init__(self, scratch, *args, **kwargs):
        Sensor.__init__(self, scratch, *args, **kwargs)
        GPIO.setmode(GPIO.BCM)

        self.threshold = 1
        self.lastValue = 0

        self.pin = eval(self.data)

    def setRegister(self, key, value):
        if key == "threshold":
            self.threshold = eval(value)

    def tick(self):
        value = self.RCtime(self.pin)
        if abs(value-self.lastValue) > self.threshold:
            self.scratch.updateSensor("light", value)
            self.scratch.broadcast("light-updated")
            self.lastValue = value

    def RCtime(self, pin):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.01)

        GPIO.setup(pin, GPIO.IN)
        measurement = 0
        while (GPIO.input(pin) == GPIO.HIGH):
            measurement += 1

        return measurement