from scratchcomms import ScratchComms
from sensormanager import SensorManager
from event.eventhandler import EventHandler
from tkinter import *
import time, traceback, sys
from drivers.lb1930mc import LB1930MC
from drivers.piklet import Piklet


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
        self.startupEdgeCase()
        self.running = True
        self.loop()

    def startupEdgeCase(self):
        LB1930MC(pins=Piklet.pins["ML"]).stop()


    def stop(self, window=None):
        """
        Call to stop server
        :return:
        """
        if window:
            window.destroy()
        self.running = False
        #self.createInfoDialog("The Piklet has stopped running.")

    def onScratchDisconnect(self, data):
        self.connected = False
        self.sensors.stop()
        print("Scratch disconnected")

    def createInfoDialog(self, message):
        root = Tk()
        root.title("Piklet")
        Label(root, text=message).pack(padx=5)
        b = Button(root, text="OK", command=lambda: root.destroy())
        b.pack(pady=5)
        root.mainloop()

    def createSmallErrorDialog(self, message):
        root = Tk()
        root.title("Piklet")
        Label(root, text="The Piklet code has crashed!").pack(padx=5)
        b = Button(root, text="Ignore", command=lambda: root.destroy())
        b.pack(pady=5)
        b = Button(root, text="View Error", command=lambda: self.createErrorDialog(message))
        b.pack(pady=5)
        b = Button(root, text="Stop Piklet", command=lambda: self.stop(window=root))
        b.pack(pady=5)
        root.mainloop()

    def createErrorDialog(self, message):
        root = Tk()
        root.title("Piklet")
        Label(root, text=message, justify=LEFT).pack(padx=5)
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
            if self.connected == False:
                self.connected = self.scratch.connect()
                if self.connected:
                    #self.createInfoDialog("Piklet connected to Scratch.")
                    pass
                time.sleep(5)


            else:
                self.sensors.tick()
                self.scratch.tick()

                if self.connected == False:
                    break

            time.sleep(0.05)

#Called if file not imported by another python program
if __name__ == "__main__":
    server = Server()
    server.running = True

    errorCount = 0

    while server.running:
        try:
            server.start()
        except KeyboardInterrupt:
            server.stop()
        except:
            print("Exception in user code:")
            print('-' * 60)
            print("".join(traceback.format_exception(*sys.exc_info())))
            server.createSmallErrorDialog("".join(traceback.format_exception(*sys.exc_info())))
            print('-' * 60)
            errorCount += 1