# This script is based on http://bikecalculator.com/
# cf http://bikecalculator.com/bikecalculator.js

class Tire:
    # Clinchers, tubulars, MTB
    tireResistance = [0.005, 0.004, 0.012]
    def __init__(self, tireType=0):
        self.resistance = self.tireResistance[tireType]

class Rider:
    # Hoods, Bartops, Bar ends, Drops, Aerobar
    aeroValues = [0.388, 0.445, 0.420, 0.300, 0.233, 0.200]
    def __init__(self, position=3):
        self.resistance = self.aeroValues[position]

class Bike:
    def __init__(self, tire):
        self.tire = tire
        self.tranv = 0.95 # transmission efficiency

class Road:
    def __init__(self, distance, elevation=0, temperature=20, grade=0, headwind=0):
        self.grade = grade*0.01
        self.headwind = headwind/3.6
        self.distance = distance
        self.temperature = temperature
        self.elevation = elevation
