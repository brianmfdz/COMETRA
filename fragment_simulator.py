import numpy as np


class FragmentSimulator:

    G = 6.67430e-11

    def calculateGravity(
        self,
        sourceBody,
        targetPosition
    ):

        direction = (
            sourceBody.CelesPosition
            - targetPosition
        )

        distance = np.linalg.norm(
            direction
        )

        if distance == 0:
            return np.array(
                [0.0, 0.0, 0.0]
            )

        acceleration = (
            self.G
            * sourceBody.CelesMass
            * direction
            / distance**3
        )

        return acceleration

    def calculateFragmentAcceleration(
        self,
        fragment,
        solarSystem
    ):

        totalAcceleration = np.array(
            [0.0, 0.0, 0.0]
        )

        for body in solarSystem.bodies:

            if body == fragment:
                continue

            if body.CelesMass <= 0:
                continue

            acceleration = (
                self.calculateGravity(
                    body,
                    fragment.CelesPosition
                )
            )

            totalAcceleration = (
                totalAcceleration
                + acceleration
            )

        return totalAcceleration

    def step(
        self,
        fragment,
        solarSystem,
        dt,
        newTime
    ):

        oldAcceleration = (
            self.calculateFragmentAcceleration(
                fragment,
                solarSystem
            )
        )

        fragment.CelesVelocity = (
            fragment.CelesVelocity
            + 0.5
            * oldAcceleration
            * dt
        )

        newPosition = (
            fragment.CelesPosition
            + fragment.CelesVelocity
            * dt
        )

        fragment.setPosition(
            newPosition
        )

        newAcceleration = (
            self.calculateFragmentAcceleration(
                fragment,
                solarSystem
            )
        )

        fragment.CelesVelocity = (
            fragment.CelesVelocity
            + 0.5
            * newAcceleration
            * dt
        )

        fragment.trajectory.append(
            fragment.CelesPosition.copy()
        )

        fragment.trajectoryTimes.append(
            newTime
        )