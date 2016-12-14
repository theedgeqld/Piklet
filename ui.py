from tkinter import *
from server import Server
from threading import Thread
from drivers.piklet import Piklet
import os

class Application:
    def __init__(self):
        self.setupUI()

    def getFilesInDirectory(self, dir="sensors"):
        badFiles = ["__pycache__", "__init__.py", "template.py"]
        files = [f.split(".")[0] for f in os.listdir(dir) if not f in badFiles]
        files.append("motor")
        return files

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

    def runServer(self):
        def onDie():
            self.widgets["startButton"].configure(bg="lightgray")
            self.widgets["startButton"].configure(fg="black")
            self.widgets["startButtonText"].set("Run Server")

        if self.widgets["startButtonText"].get() == "Run Server":
            self.widgets["startButton"].configure(bg="green")
            self.widgets["startButton"].configure(fg="white")
            self.widgets["startButtonText"].set("Stop Server")

            self.server = Server()
            self.serverThread = Thread(target=lambda: self.server.start(onDie=onDie))
            self.serverThread.setDaemon(True)
            self.serverThread.start()
        else:
            self.server.running = False

    def getButtonEnabledToggleCallback(self, sensorName, sensorPort):
        return lambda: self.buttonEnabledToggleCallback(sensorName, sensorPort())

    def buttonEnabledToggleCallback(self, sensorName, sensorPort):
        isOn = self.widgets[sensorName]["buttonText"].get() == "Off"
        uniqueSensorID = sensorName + "_" + sensorPort

        if isOn:
            self.server.sensors.disableSensor(uniqueSensorID)
            self.widgets[sensorName]["buttonText"].set("On")
            self.widgets[sensorName]["button"].configure(bg="lightgray")
            self.widgets[sensorName]["button"].configure(fg="black")
        else:
            uniqueSensorClass = self.server.sensors.classes[sensorName]
            self.server.sensors.enableSensor(uniqueSensorID, uniqueSensorClass, data=sensorPort)

            self.widgets[sensorName]["button"].configure(bg="green")
            self.widgets[sensorName]["button"].configure(fg="white")

            self.widgets[sensorName]["buttonText"].set("Off")


    def setupUI(self):
        self.widgets = {}

        self.root = Tk()
        self.root.title("Piklet")
        sensorFrame = Frame(self.root)

        # =====[ Run Server Button]=====#
        startButtonText = StringVar()
        startButtonText.set("Run Server")
        b = Button(self.root, textvariable=startButtonText, command=self.runServer)
        b.pack()
        self.widgets["startButton"] = b
        self.widgets["startButtonText"] = startButtonText

        r = 0

        for sensor in self.getFilesInDirectory(dir="/opt/Piklet/sensors"):
            if sensor == "motor" and sensor not in self.widgets:
                motorName = "motorL"
            else:
                motorName = "motorR"
            self.widgets[motorName] = {}

            widgetDict = self.widgets[sensor]

            # =====[ Sensor Label ]=====#
            l = Label(sensorFrame, text=motorName)
            l.grid(row=r, column=0, sticky="W")
            widgetDict["label"] = l

            #=====[ Pin Option Box ]=====#
            var = StringVar(sensorFrame)
            options = self.pinsForSensor(sensor)
            option = OptionMenu(sensorFrame, var, *options)
            option.grid(row=r, column=1, sticky="ew")
            widgetDict["option"] = option

            # =====[ On/Off Button ]=====#
            btnText = StringVar()
            btnText.set("On")
            on = Button(sensorFrame, textvariable=btnText, command=self.getButtonEnabledToggleCallback(sensor, var.get))
            on.grid(row=r, column=2)
            widgetDict["buttonText"] = btnText
            widgetDict["button"] = on

            r += 1

        sensorFrame.pack(side=LEFT)
        self.root.mainloop()


if __name__ == "__main__":
    app = Application()