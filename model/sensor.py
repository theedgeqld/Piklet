from threading import Thread

class Sensor:
    def __init__(self, scratch, data=None):
        """
        Constructor for the Sensor type
        :param scratch: Scratch communications object
        :param data: Any extra data, typically unique to the sensor object (typically sensor pin)
        """

        self.scratch = scratch
        self.data = data

    def start(self):
        """
        Called when the sensor is enabled
        :return:
        """
        pass

    def stop(self):
        """
        Called when the sensor is disabled
        :return:
        """
        pass

    def setRegister(self, key, value):
        """
        Called when a variable with the format of:
            piklet_<sensorClass>_<sensorID>_<register>
        Is updated with a new value.

        :param key: Register to update
        :param value: Value to update register to
        :return:
        """
        print("Register changed", key, value)

    def tick(self):
        """
        Called every loop of the main loop
        :return:
        """
        raise NotImplementedError

class ThreadedSensor:
    def __init__(self, scratch, data=None):
        """
        Constructor for the ThreadedSensor type
        :param scratch: Scratch communications object
        :param data: Any extra data, typically unique to the sensor object (typically sensor pin)
        """

        self.running = False
        self.scratch = scratch
        self.data = data

    def start(self):
        """
        Called when the sensor is enabled
        :return:
        """
        self.running = True
        self.thread = Thread(target=self.loop)
        self.thread.setDaemon(True)
        self.thread.start()

    def stop(self):
        """
        Called when the sensor is disabled
        This does not garantee that the thread loop stops running
        :return:
        """
        self.running = False

    def setRegister(self, key, value):
        """
        Called when a variable with the format of:
            piklet_<sensorClass>_<sensorID>_<register>
        Is updated with a new value.

        :param key: Register to update
        :param value: Value to update register to
        :return:
        """
        print("Register changed", key, value)

    def loop(self):
        """
        This loop contains the blocking sensor-checking code
        :return:
        """
        raise NotImplementedError