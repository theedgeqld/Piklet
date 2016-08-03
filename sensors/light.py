from model.sensor import Sensor
import RPi.GPIO as GPIO
import time

class light(Sensor):
    def __init__(self, scratch, *args, **kwargs):
        Sensor.__init__(self, scratch, *args, **kwargs)
        GPIO.setmode(GPIO.BCM)

    def tick(self):
        self.scratch.updateSensor("light", self.RCtime(13))
        self.scratch.broadcast("light-updated")

    def RCtime(self, pin):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.01)

        GPIO.setup(pin, GPIO.IN)
        measurement = 0
        while (GPIO.input(pin) == GPIO.HIGH):
            measurement += 1

        return measurement