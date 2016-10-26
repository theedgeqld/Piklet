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
    }

    @staticmethod
    def getPinGroup(id):
        return Piklet.pins[id]