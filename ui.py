from tkinter import *
from drivers.piklet import Piklet
import os

class Application:
    def __init__(self):
        self.setupUI()

    def getFilesInDirectory(self, dir="sensors"):
        badFiles = ["__pycache__", "__init__.py", "template.py"]
        files = [f.split(".")[0] for f in os.listdir(dir) if not f in badFiles]
        return files

    def addSensorUI(self, sensorName, onCallback=lambda x: -1, offCallback=lambda x: -1, options=[]):
        ultrasonicFrame = Frame(self.root)
        frame = Frame(self.root)

        Label(ultrasonicFrame, text=sensorName).pack(side=LEFT)

        var = StringVar(ultrasonicFrame)

        option = OptionMenu(ultrasonicFrame, var, *options)
        option.pack(side=LEFT)

        on = Button(ultrasonicFrame, text="On", command=lambda: onCallback(sensorName, var.get()))
        on.pack(side=LEFT)

        off = Button(ultrasonicFrame, text="Off", command=lambda: offCallback(sensorName, var.get()))
        off.pack(side=LEFT)

        ultrasonicFrame.pack()

    def getSensorPinGroup(self, sensor):
        exec("from sensors.{} import {}".format(sensor, sensor))
        class_ = eval(sensor)
        try:
            return class_.pinGroup
        except:
            return None

    def pinsForSensor(self, sensor):
        opts = Piklet.pinsInGroup(self.getSensorPinGroup(sensor))
        return opts


    def setupUI(self):
        self.root = Tk()
        self.root.title("Piklet")

        for sensor in self.getFilesInDirectory(dir="sensors"):
            def sensorCallback(sensorName, sensorPort):
                print(sensorName, sensorPort)

            options = self.pinsForSensor(sensor)
            self.addSensorUI(sensor, onCallback=sensorCallback, options=options)

        self.root.mainloop()


if __name__ == "__main__":
    app = Application()