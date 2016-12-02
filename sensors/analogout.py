from model.sensor import Sensor
import RPi.GPIO as GPIO
import time
from drivers.piklet import Piklet

class analogout(Sensor):
    pinGroup = "digital"

    def __init__(self, scratch, *args, **kwargs):
        Sensor.__init__(self, scratch, *args, **kwargs)
        GPIO.setmode(GPIO.BCM)

        self.pins = Piklet.pins[self.data]
        # First pin if there are two gets given preference
        self.pin = self.pins[0]

        GPIO.setup(self.pin, GPIO.output)
        self.duty = GPIO.PWM(self.pins[0], 50)
        self.duty.start(0)

    def setRegister(self, key, value):
        if key == "value":
            self.value = eval(value)

            self.value = 100 if self.value > 100 else self.value
            self.value = 0 if self.value < 0 else self.value

            self.duty.ChangeDutyCycle(self.value)