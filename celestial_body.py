class CelestialBody:
    def __init__(self, CelesName, CelesPosition, CelesVelocity=(0, 0, 0)):
        self.CelesName = CelesName
        self.CelesPosition = CelesPosition
        self.CelesVelocity = CelesVelocity

    def setPosition(self, newPosition):
        self.CelesPosition = newPosition


class Planet(CelestialBody):
    def __init__(self, CelesName, CelesPosition, CelesVelocity=(0, 0, 0)):
        super().__init__(CelesName, CelesPosition, CelesVelocity)

    def showInfo(self):
        print(f"Name: {self.CelesName}, Position: {self.CelesPosition}, Velocity: {self.CelesVelocity}")


class Comet(CelestialBody):
    def __init__(self, CelesName, CelesPosition, CometID, CelesVelocity=(0, 0, 0)):
        super().__init__(CelesName, CelesPosition, CelesVelocity)
        self.CometID = CometID

    def showInfo(self):
        print(
            f"Name : {self.CelesName}, Position: {self.CelesPosition}, velocity: {self.CelesVelocity}, Comet ID: {self.CometID}"
        )