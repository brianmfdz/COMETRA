class Simulator:
    def __init__(self, SolarSystem, PhysicsModel):
        self.solarSystem = SolarSystem
        self.physicsModel = PhysicsModel
        self.currentTime = 0

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

        self.currentTime = self.currentTime + dt

    def simulate(self, duration, dt):

        targetTime = self.currentTime + duration

        while self.currentTime < targetTime:

            remainingTime = targetTime - self.currentTime

            stepTime = min(
                dt,
                remainingTime
            )

            self.step(stepTime)

    def simulateUntil(self, targetTime, dt):

        while self.currentTime < targetTime:

            remainingTime = targetTime - self.currentTime

            stepTime = min(
                dt,
                remainingTime
            )

            self.step(stepTime)

    def simulateWithFragmentation(
        self,
        comet,
        fragmentationEvent,
        fragmentationModel,
        endTime,
        dt
    ):

        self.simulateUntil(
            fragmentationEvent.fragmentationTime,
            dt
        )

        fragments = fragmentationModel.createFragments(
            comet,
            fragmentationEvent.separationVelocities
        )

        for fragment in fragments:
            self.solarSystem.bodies.append(fragment)

        self.simulateUntil(
            endTime,
            dt
        )

        return fragments