from gpiozero import DistanceSensor
from time import sleep

class Distance:

    def __init__(self):
        self.Tr = 23
        self.Ec = 24
        self.sensor = DistanceSensor(echo=self.Ec, trigger=self.Tr, max_distance=2)  # Maximum detection distance 2m.

    # Get the distance of ultrasonic detection.
    def checkdist(self):
        return (self.sensor.distance) * 1000  # Unit: mm

if __name__ == "__main__":
    distance_sensor = Distance()
    while True:
        distance = distance_sensor.checkdist()
        print("%.2f mm" % distance)
        sleep(0.05)