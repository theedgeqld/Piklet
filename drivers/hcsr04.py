import RPi.GPIO as GPIO
import time

class HCSR04:
    def __init__(self, pins=(24, 25)):
        self.triggerPin, self.echoPin = pins
        self.initPins()

    def initPins(self):
        """
        Initializes all the pins for operation
        :return:
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.triggerPin, GPIO.OUT)
        GPIO.setup(self.echoPin, GPIO.IN)

    def get(self):
        """
        Gets the distance read by US sensor
        :return:
        """
        self.sendPing()
        t = self.getPingDuration()
        distance = self.getDistance(t)
        if distance > 5500:
            return self.get()
        else:
            return distance

    def settleSensor(self):
        """
        Settles the sensor down by pulling trigger pin low (should be done by default?)
        :return:
        """
        GPIO.output(self.triggerPin, False)
        time.sleep(2)

    def sendPing(self):
        """
        Sends a ping through the US sensor
        :return:
        """
        GPIO.output(self.triggerPin, True)
        time.sleep(0.0001)
        GPIO.output(self.triggerPin, False)

    def getPingDuration(self):
        """
        Times the pulse
        :return: pulse time in 10ths of a ms (?)
        """
        while GPIO.input(self.echoPin) == 0:
            pulseStart = time.time()

        while GPIO.input(self.echoPin) == 1:
            pulseEnd = time.time()

        return pulseEnd - pulseStart

    def getDistance(self, pulseDuration):
        """
        Gets the distance
        :param pulseStart:
        :param pulseEnd:
        :return:
        """
        return round(pulseDuration * 17160, 2)





