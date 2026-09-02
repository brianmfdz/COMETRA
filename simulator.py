class Simulator:
    def __init__(self, SolarSystem, PhysicsModel):
        self.solarSystem = SolarSystem
        self.physicsModel = PhysicsModel

    def calculateAccelerations(self):
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

        return accelerations

    def step(self, dt):

        oldAccelerations = self.calculateAccelerations()

        for i, body in enumerate(self.solarSystem.bodies):

            if body.CelesName == "Sun":
                continue

            body.CelesVelocity = (
                body.CelesVelocity
                + 0.5 * oldAccelerations[i] * dt
            )

            newPosition = (
                body.CelesPosition
                + body.CelesVelocity * dt
            )

            body.setPosition(newPosition)

            # Save the new position
            body.trajectory.append(
                body.CelesPosition.copy()
            )

        newAccelerations = self.calculateAccelerations()

        for i, body in enumerate(self.solarSystem.bodies):

            if body.CelesName == "Sun":
                continue

            body.CelesVelocity = (
                body.CelesVelocity
                + 0.5 * newAccelerations[i] * dt
            )