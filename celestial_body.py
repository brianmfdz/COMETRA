import numpy as np


class CelestialBody:
    def __init__(self, CelesName, CelesPosition, CelesVelocity=(0, 0, 0)):
        self.CelesName = CelesName
        self.CelesPosition = np.array(CelesPosition, dtype=float)
        self.CelesVelocity = np.array(CelesVelocity, dtype=float)

    def setPosition(self, newPosition):
        self.CelesPosition = np.array(newPosition, dtype=float)


class Planet(CelestialBody):
    def __init__(self, CelesName, CelesPosition, CelesVelocity=(0, 0, 0)):
        super().__init__(CelesName, CelesPosition, CelesVelocity)

    def showInfo(self):
        print(
            f"Name: {self.CelesName}, "
            f"Position: {self.CelesPosition}, "
            f"Velocity: {self.CelesVelocity}"
        )


class Comet(CelestialBody):
    def __init__(
        self,
        CelesName,
        CelesPosition,
        CometID,
        CelesVelocity=(0, 0, 0)
    ):
        super().__init__(CelesName, CelesPosition, CelesVelocity)
        self.CometID = CometID

    def showInfo(self):
        print(
            f"Name: {self.CelesName}, "
            f"Position: {self.CelesPosition}, "
            f"Velocity: {self.CelesVelocity}, "
            f"Comet ID: {self.CometID}"
        )