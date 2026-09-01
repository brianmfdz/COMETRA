class Simulator:
    def __init__(self, SolarSystem, PhysicsModel):
        self.solarSystem = SolarSystem
        self.physicsModel = PhysicsModel

    def step(self, dt):

        accelerations = []

        for body in self.solarSystem.bodies:

            totalAcceleration = 0

            for otherBody in self.solarSystem.bodies:

                if body == otherBody:
                    continue

                acceleration = self.physicsModel.calculateGravity(
                    otherBody,
                    body.CelesPosition
                )

                totalAcceleration = (
                    totalAcceleration + acceleration
                )

            accelerations.append(totalAcceleration)

        for i, body in enumerate(self.solarSystem.bodies):

            body.CelesVelocity = (
                body.CelesVelocity
                + accelerations[i] * dt
            )

            newPosition = (
                body.CelesPosition
                + body.CelesVelocity * dt
            )

            body.setPosition(newPosition)