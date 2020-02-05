# This script is based on http://bikecalculator.com/
# cf http://bikecalculator.com/bikecalculator.js

class Tire:
    tireResistance = [0.005, 0.004, 0.012]
    def __init__(self, tireType=0):
        self.resistance = self.tireResistance[tireType]
    def getResistance(self):
        return self.resistance

print(Tire(1).getResistance())