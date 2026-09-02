import numpy as np


class TrajectoryAnalysis:

    def calculateClosestApproach(
        self,
        targetBody,
        movingBody
    ):

        minimumDistance = None
        closestPoint = None

        for i, position in enumerate(
            movingBody.trajectory
        ):

            targetPosition = targetBody.trajectory[i]

            distance = np.linalg.norm(
                position - targetPosition
            )

            if minimumDistance is None:
                minimumDistance = distance
                closestPoint = i

            elif distance < minimumDistance:
                minimumDistance = distance
                closestPoint = i

        return minimumDistance, closestPoint