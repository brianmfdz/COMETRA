class SolarSystem:
    def __init__(self, bodies):
        self.bodies = bodies

    def showInfo(self):
        for body in self.bodies:
            body.showInfo()