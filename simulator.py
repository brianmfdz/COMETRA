class Simulator:
    def __init__(self, SolarSystem, PhysicsModel):
        self.solarSystem = SolarSystem
        self.physicsModel = PhysicsModel

    def step(self, dt):
        for body in self.solarSystem.bodies:

            acceleration = self.physicsModel.calculateGravity(
                self.solarSystem.bodies[0],
                body.CelesPosition
            )

            body.CelesVelocity = (
                body.CelesVelocity + acceleration * dt
            )

            newPosition = (
                body.CelesPosition
                + body.CelesVelocity * dt
            )

            body.setPosition(newPosition)