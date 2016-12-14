from model.sensor import Sensor, ThreadedSensor
from event.eventhandler import EventHandler
import os, traceback
from tkinter import *

class SensorManager:
    def __init__(self, scratch):
        """
        Constructor for SensorManager

        Adds a listener to the variable-updated event.
        This event is called when scratch updates a variable.
        In this case, the sensor manager checks to see whether
        the variable was a sensor-enable register. If so, it enables
        the specified sensor.

        :param scratch:
        """

        self.sensors = {}
        self.scratch = scratch

        self.classes = self.getSensorClasses()

        EventHandler.addListener("variable-updated", self.onVariableUpdated)

    def getSensorFiles(self):
        """
        Gets a list of sensor drivers located in the ./sensors folder
        :return:
        """

        files = os.listdir(__file__.replace("sensormanager.py", "")+"sensors/")
        sensorDrivers = [file.replace(".py", "") for file in files if file.endswith(".py") and not file == "__init__.py"]
        return sensorDrivers

    def getSensorClasses(self):
        """
        Imports sensor drivers in ./sensors folder, and then gets their sensor driver object
        :return: Dictionary of sensor driver classes
        """

        files = self.getSensorFiles()
        classes = {}
        for file in files:
            exec("from sensors.{} import {}".format(file, file))
            class_ = eval(file)
            classes[class_.__name__] = class_
        return classes

    def isSensorThreaded(self, sensorClass):
        """
        Returns boolean whether specified sensor class is threaded
        :param sensorClass:
        :return:
        """

        return issubclass(sensorClass, ThreadedSensor)

    def onVariableUpdated(self, data):
        """
        Called when a variable is updated in scratch.
        Listener added in constructor.

        Enables or disables specified sensors, else:
        Updates the register of specified sensors

        Key Format: piklet_<sensorClass>_<sensorID>_<register>

        :param data: key, value
        :return:
        """

        key, value = data

        #If the variable is pertaining to us,
        if key.startswith("piklet_"):

            command, sensorClass, sensorID, sensorRegister = key.split("_")

            uniqueSensorID = sensorClass + "_" + sensorID
            uniqueSensorClass = self.classes[sensorClass]

            #And if the user is requesting a sensor is enabled/disabled,
            if sensorRegister == "enabled":

                #Enable the sensor if the value is 1
                if value == "1":
                    self.enableSensor(uniqueSensorID, uniqueSensorClass, data=sensorID)

                #Disable the sensor if the value is 0
                elif value == "0":
                    self.disableSensor(uniqueSensorID)

            #If all else fails, just set the specified register
            else:
                try:
                    self.sensors[uniqueSensorID].setRegister(sensorRegister, value)
                except KeyError:
                    print("The specified sensor has not been enabled.")

    def enableSensor(self, sensorID, sensorClass, data=None):
        """
        Instantiates a sensor with a specified ID and class
        :param sensorID:
        :param sensorClass:
        :param data:
        """
        try:
            sensor = sensorClass(self.scratch, data=data)
            sensor.start()
            self.sensors[sensorID] = sensor
            print("Enabled {}".format(sensorID))
        except:
            msg = ("="*10)+"[ Sensor Error ]"+("="*10)

            print(msg)
            traceback.print_exc()
            print("="*len(msg))

            self.createInfoDialog("Error enabling {}".format(sensorID))

    def createInfoDialog(self, message):
        root = Tk()
        root.title("Piklet")
        Label(root, text=message).pack(padx=5)
        b = Button(root, text="OK", command=lambda: root.destroy())
        b.pack(pady=5)
        root.mainloop()

    def disableSensor(self, sensorID):
        """
        Disables the specified sensor, or errors if it doesn't exist
        :param sensorID:
        """
        try:
            self.sensors[sensorID].stop()
            del self.sensors[sensorID]
            print("Disabled {}".format(sensorID))
        except:
            print("{} sensor has not been enabled.".format(sensorID))

    def stop(self):
        for sensorID in self.sensors:
            self.disableSensor(sensorID)

    def tick(self):
        """
        Called every run of the main loop.
        Calls the tick functions of each enabled sensor, if it is not threaded
        :return:
        """
        for sensorName in self.sensors:
            sensor = self.sensors[sensorName]
            if issubclass(sensor.__class__, Sensor):
                try:
                    sensor.tick()
                except IOError:
                    print("Error with sensor {}. Stopping".format(sensorName))
                    del self.sensors[sensorName]
                    break
            else:
                pass