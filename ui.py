from tkinter import *
from drivers.piklet import Piklet

root = Tk()
root.title("Piklet")

class Application:
    def __init__(self):
        pass

def addSensorUI(self, sensorName, onCallback, offCallbackXXZqdswA!Qs1   2EQ):
        frame = Frame(root)

        Label(ultrasonicFrame, text="Ultrasonic").pack(side=LEFT)

        options = list(Piklet.pins.keys())
        var = StringVar(ultrasonicFrame)

        option = OptionMenu(ultrasonicFrame, var, *options)
        option.pack(side=LEFT)

        on = Button(ultrasonicFrame, text="On", command=lambda: root.destroy())
        on.pack(side=LEFT)

        off = Button(ultrasonicFrame, text="Off", command=lambda: root.destroy())
        off.pack(side=LEFT)

        ultrasonicFrame.pack()

    def test(self):
        print("Called")


def addUltrasonicUI():
    ultrasonicFrame = Frame(root)
    Label(ultrasonicFrame, text="Ultrasonic").pack(side=LEFT)

    options = list(Piklet.pins.keys())
    var = StringVar(ultrasonicFrame)

    option = OptionMenu(ultrasonicFrame, var, *options)
    option.pack(side=LEFT)

    on = Button(ultrasonicFrame, text="On", command=lambda: root.destroy())
    on.pack(side=LEFT)

    off = Button(ultrasonicFrame, text="Off", command=lambda: root.destroy())
    off.pack(side=LEFT)

    ultrasonicFrame.pack()

addUltrasonicUI()

root.mainloop()