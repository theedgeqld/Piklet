class Piklet:
    pins = {
        "SPI0": (10, 9, 11, 8), #Dedicated SPI
        "D2": (25, 24),
        "D3": (13, 16),
        "D4": (2, 3),
        "D5": (5, 6),
        "D6": (21, 26),
        "D7": (19, 20),
        "D8": (14, 15),
        "SPI1": (10, 9, 11, 7), #Analog
        "M1": (17, 4),
        "M2": (22, 27),
        "M3": (23, 18),
        "ML": (17, 4),
        "MR": (22, 27),
        "MC": (23, 18),
        "SOUND": 7,
        "STATUS_LED": [6],
        "UART": "/dev/ttyAMA0"
    }

    pinGroups = {
        "digital": [
            "D2",
            "D3",
            "D4",
            "D5",
            "D6",
            "D7",
            "D8",
        ],
        "SPI": [
            "SPI0",
            "SPI1"
        ],
        "motor": [
            "M1",
            "M2",
            "M3",
            "ML",
            "MC",
            "MR"
        ],
        "light": [
            "STATUS_LED"
        ],
        "analog": [
            "SOUND"
        ],
        "serial": [
            "UART"
        ]
    }

    @staticmethod
    def getPinGroup(id):
        return Piklet.pins[id]

    def groupContains(self, group, pin):
        if group == None:
            return True

        if pin in Piklet.pinGroups[group]:
            return True
        else:
            return False

    def pinsInGroup(group):
        if group == None:
            return list(Piklet.pins.keys())

        else:
            return Piklet.pinGroups[group]