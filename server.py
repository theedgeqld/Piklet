from scratchcomms import ScratchComms
from sensormanager import SensorManager
from event.eventhandler import EventHandler
from tkinter import *
import time, threading


class Server:
    def __init__(self):
        """
        Initiates Piklet Sensor server
        """
        self.running = False

        EventHandler.addListener("scratch-disconnect", self.onScratchDisconnect)
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

    def onScratchDisconnect(self, data):
        self.connected = False
        print("Scratch disconnected")

    def createDialog(self, message):
        root = Tk()
        root.title("Piklet")
        Label(root, text=message).pack(padx=5)
        b = Button(root, text="OK", command=lambda: root.destroy())
        b.pack(pady=5)
        root.mainloop()

    def loop(self):
        """
        Runs while self.stop has not been called.

        Should run in a non-blocking fashion;
        None of the code contained within should wait
        siginificant amounts of time for IO operations.
        :return:
        """

        while self.running:
            while self.connected == False:
                self.connected = self.scratch.connect()
                if self.connected:
                    self.createDialog("Piklet connected to Scratch.")
                else:
                    pass
                time.sleep(5)


            else:
                self.sensors.tick()
                self.scratch.tick()

            time.sleep(0.05)

class MyDialog:

    def __init__(self, parent):
        top = self.top = Toplevel(parent)

        Label(top, text="Piklet software has connected to Scratch").pack()
        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        self.top.destroy()
        self.destr

#Called if file not imported by another python program
if __name__ == "__main__":
    server = Server()
    server.start()