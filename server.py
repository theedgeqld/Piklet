from scratchcomms import ScratchComms
from sensormanager import SensorManager
import sys, time, os


class Server:
    def __init__(self):
        """
        Initiates Piklet Sensor server
        """
        self.running = False

        self.scratch = ScratchComms("localhost")
        self.connected = False

        self.sensors = SensorManager(self.scratch)

    def start(self):
        """
        Called when server starts
        :return:
        """
        self.running = True
        self.loop()

    def stop(self):
        """
        Call to stop server
        :return:
        """
        self.running = False

    def loop(self):
        """
        Runs while self.stop has not been called.

        Should run in a non-blocking fashion;
        None of the code contained within should wait
        siginificant amounts of time for IO operations.
        :return:
        """

        while self.running:

            if not self.connected:
                self.connected = self.scratch.connect()

                if self.connected:
                    print("Connected to scratch!")

            else:
                self.sensors.tick()
                self.scratch.tick()

            time.sleep(0.05)

#Called if file not imported by another python program
if __name__ == "__main__":
    server = Server()
    server.start()