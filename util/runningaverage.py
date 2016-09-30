class RunningAverage:
    def __init__(self, length=10):
        self.numbers = []
        self.length = length

    def add(self, value):
        self.numbers.append(value)
        if len(self.numbers) > self.length:
            del self.numbers[0]


    def getAverage(self):
        return sum(self.numbers) / len(self.numbers)