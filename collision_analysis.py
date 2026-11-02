import numpy as np


class CollisionAnalysis:
    BODY_RADII = {
        "Sun": 6.957e8,
        "Mercury": 2.4397e6,
        "Venus": 6.0518e6,
        "Earth": 6.371e6,
        "Mars": 3.3895e6,
        "Jupiter": 6.9911e7,
        "Saturn": 5.8232e7,
        "Uranus": 2.5362e7,
        "Neptune": 2.4622e7
    }

    def __init__(self, fragmentRadius=1000):
        self.fragmentRadius = fragmentRadius

    def _buildStateIndex(self, body):
        return {
            timestamp: (index, position)
            for index, (timestamp, position) in enumerate(
                zip(body.trajectoryTimes, body.trajectory)
            )
        }

    def _firstContact(self, firstRelativePosition, relativeDisplacement, radius):
        firstDistance = np.linalg.norm(firstRelativePosition)
        if firstDistance <= radius:
            return 0.0

        displacementSquared = np.dot(
            relativeDisplacement,
            relativeDisplacement
        )
        if displacementSquared == 0:
            return None

        closestFraction = np.clip(
            -np.dot(firstRelativePosition, relativeDisplacement)
            / displacementSquared,
            0.0,
            1.0
        )
        closestPosition = (
            firstRelativePosition
            + closestFraction * relativeDisplacement
        )
        if np.dot(closestPosition, closestPosition) > radius**2:
            return None

        a = displacementSquared
        b = 2 * np.dot(
            firstRelativePosition,
            relativeDisplacement
        )
        c = np.dot(
            firstRelativePosition,
            firstRelativePosition
        ) - radius**2
        discriminant = b**2 - 4 * a * c
        if discriminant < 0:
            return None

        return float(np.clip(
            (-b - np.sqrt(discriminant)) / (2 * a),
            0.0,
            1.0
        ))

    def _detectPair(
        self,
        firstBody,
        secondBody,
        collisionRadius,
        ignoreInitialOverlap=False,
        secondStates=None,
        firstRadius=None,
        secondRadius=None
    ):
        if secondStates is None:
            secondStates = self._buildStateIndex(secondBody)

        initialOverlap = False
        if ignoreInitialOverlap and firstBody.trajectory:
            initialTime = firstBody.trajectoryTimes[0]
            initialState = secondStates.get(initialTime)
            if initialState is not None:
                initialOverlap = (
                    np.linalg.norm(
                        firstBody.trajectory[0] - initialState[1]
                    ) <= collisionRadius
                )

        collisions = []
        for index in range(len(firstBody.trajectory) - 1):
            startTime = firstBody.trajectoryTimes[index]
            endTime = firstBody.trajectoryTimes[index + 1]
            startState = secondStates.get(startTime)
            endState = secondStates.get(endTime)
            if startState is None or endState is None:
                continue

            startBodyIndex, startBodyPosition = startState
            endBodyIndex, endBodyPosition = endState
            if endBodyIndex != startBodyIndex + 1:
                continue

            firstStart = firstBody.trajectory[index]
            firstEnd = firstBody.trajectory[index + 1]
            relativeStart = firstStart - startBodyPosition
            relativeEnd = firstEnd - endBodyPosition
            if initialOverlap:
                if np.linalg.norm(relativeEnd) > collisionRadius:
                    initialOverlap = False
                continue

            fraction = self._firstContact(
                relativeStart,
                relativeEnd - relativeStart,
                collisionRadius
            )
            if fraction is None:
                continue

            collisionTime = startTime + (endTime - startTime) * fraction
            firstPosition = firstStart + fraction * (firstEnd - firstStart)
            secondPosition = (
                startBodyPosition
                + fraction * (endBodyPosition - startBodyPosition)
            )
            pointIndex = startBodyIndex + fraction
            if firstRadius is None or secondRadius is None:
                contactPosition = (firstPosition + secondPosition) / 2
            else:
                contactPosition = firstPosition + (
                    (secondPosition - firstPosition)
                    * firstRadius
                    / (firstRadius + secondRadius)
                )

            collisions.append({
                "bodyA": firstBody.CelesName,
                "bodyB": secondBody.CelesName,
                "time": collisionTime,
                "positionA": firstPosition,
                "positionB": secondPosition,
                "position": contactPosition,
                "collisionRadius": collisionRadius,
                "pointIndex": pointIndex
            })
            initialOverlap = (
                np.linalg.norm(relativeEnd) <= collisionRadius
            )

        return collisions

    def findCollisions(self, fragments, targetBodies):
        collisions = []
        targetStates = []

        for target in targetBodies:
            targetRadius = self.BODY_RADII.get(target.CelesName)
            if targetRadius is None:
                continue

            targetStates.append(
                (
                    target,
                    targetRadius,
                    self._buildStateIndex(target)
                )
            )

        for fragment in fragments:
            for target, targetRadius, targetState in targetStates:
                collisions.extend(self._detectPair(
                    fragment,
                    target,
                    self.fragmentRadius + targetRadius,
                    secondStates=targetState,
                    firstRadius=self.fragmentRadius,
                    secondRadius=targetRadius
                ))

        for index, fragment in enumerate(fragments):
            for otherFragment in fragments[index + 1:]:
                collisions.extend(self._detectPair(
                    fragment,
                    otherFragment,
                    self.fragmentRadius * 2,
                    ignoreInitialOverlap=True,
                    firstRadius=self.fragmentRadius,
                    secondRadius=self.fragmentRadius
                ))

        collisions.sort(key=lambda collision: collision["time"])
        return collisions