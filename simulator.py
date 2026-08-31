class Simulator:
    def __init__(self, SolarSystem):
        self.solarSystem = SolarSystem

    def step(self, dt):
        for body in self.solarSystem.bodies:
            currentPosition = body.CelesPosition
            currentVelocity = body.CelesVelocity

            newPosition = currentPosition + currentVelocity * dt

            body.setPosition(newPosition)