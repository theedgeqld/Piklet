from model.sensor import Sensor
import RPi.GPIO as GPIO
from drivers.piklet import Piklet

class digitalout(Sensor):
    def __init__(self, scratch, *args, **kwargs):
        Sensor.__init__(self, scratch, *args, **kwargs)
        GPIO.setmode(GPIO.BCM)

        self.pins = Piklet.pins[self.data]

        #First pin if there are two gets given preference
        self.pin = self.pins[0]

        GPIO.setup(self.pin, GPIO.output)

    def setRegister(self, key, value):
        if key == "value":

            self.value = eval(value)
            self.value = GPIO.HIGH if self.value == 0 else GPIO.LOW

            GPIO.output(self.pin, self.value)