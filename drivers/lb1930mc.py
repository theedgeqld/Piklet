"""
Uses servoblaster user driver to control PWM
(frees up requirement for hardware PWM pin)

https://github.com/richardghirst/PiBits/tree/master/ServoBlaster
"""

import RPi.GPIO as GPIO

class LB1930MC:
    def __init__(self, pins):
        self.pins = pins

        self.initPins()

    def initPins(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.pins[0], GPIO.OUT)
        GPIO.setup(self.pins[1], GPIO.OUT)

        self.forwardDuty = GPIO.PWM(self.pins[0], 50)
        self.reverseDuty = GPIO.PWM(self.pins[1], 50)

        self.forwardDuty.start(0)
        self.reverseDuty.start(0)

        self.set(0)


    def set(self, speed):
        if speed > 0:
            self.forwardDuty.ChangeDutyCycle(speed)
            self.reverseDuty.ChangeDutyCycle(0)
        else:
            self.forwardDuty.ChangeDutyCycle(0)
            self.reverseDuty.ChangeDutyCycle(abs(speed))

    def stop(self):
        self.set(0)
        GPIO.cleanup()




