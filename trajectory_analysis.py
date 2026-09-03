import numpy as np


class TrajectoryAnalysis:

    def calculateClosestApproach(
        self,
        targetBody,
        movingBody
    ):

        minimumDistance = None
        closestPoint = None
        closestTime = None

        targetStates = {}

        for i, time in enumerate(
            targetBody.trajectoryTimes
        ):

            targetStates[time] = (
                targetBody.trajectory[i]
            )

        for i, time in enumerate(
            movingBody.trajectoryTimes
        ):

            if time not in targetStates:
                continue

            movingPosition = (
                movingBody.trajectory[i]
            )

            targetPosition = (
                targetStates[time]
            )

            distance = np.linalg.norm(
                movingPosition - targetPosition
            )

            if minimumDistance is None:

                minimumDistance = distance
                closestPoint = i
                closestTime = time

            elif distance < minimumDistance:

                minimumDistance = distance
                closestPoint = i
                closestTime = time

        if minimumDistance is None:

            raise ValueError(
                "No matching timestamps were found "
                "between the trajectories."
            )

        return (
            minimumDistance,
            closestPoint,
            closestTime
        )