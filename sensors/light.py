from model.sensor import Sensor
import RPi.GPIO as GPIO
import time
from drivers.piklet import Piklet

"""
BE AWARE:
B = GND
R = SIG
W = SIG
"""

class light(Sensor):
    pinGroup = "digital"

    def __init__(self, scratch, *args, **kwargs):
        Sensor.__init__(self, scratch, *args, **kwargs)
        GPIO.setmode(GPIO.BCM)

        self.threshold = 0.5
        self.lastValue = 0

        self.pin = Piklet.pins[self.data][0]
        self.pwr = Piklet.pins[self.data][1]

    def setRegister(self, key, value):
        if key == "threshold":
            self.threshold = eval(value)

    def tick(self):
        value = self.RCtime(self.pin)
        print(value)
        if abs(value-self.lastValue) > self.threshold:
            self.scratch.updateSensor("light", value)
            self.scratch.broadcast("light-updated")
            self.lastValue = value

    def RCtime(self, pin):
        """
        Return ms of time taken * 4
        :param pin:
        :return:
        """
        GPIO.setup(self.pwr, GPIO.OUT)
        GPIO.setup(pin, GPIO.OUT)

        GPIO.output(self.pwr, GPIO.HIGH)
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.001)

        time_start = time.time()
        GPIO.setup(pin, GPIO.IN)
        while (GPIO.input(pin) == GPIO.HIGH):
            pass
        time_end = time.time()
        GPIO.output(self.pwr, GPIO.LOW)

        TO_MS = 1000
        MULTIPLIER = 4.5        #Multiplier just makes the ms value higher than 22 to make it easier to work wi

        time_dif = time_end - time_start
        return round(time_dif*TO_MS*MULTIPLIER, 2)
