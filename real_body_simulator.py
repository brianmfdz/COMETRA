class RealBodySimulator:

    def updateBodies(
        self,
        solarSystem,
        jplEphemeris,
        point
    ):

        referenceTime = jplEphemeris.getState(
            "Earth",
            point
        )["time"]
        bodyNames = set(
            jplEphemeris.getBodyNames()
        )

        for body in solarSystem.bodies:

            if body.CelesName not in bodyNames:
                if body.CelesName == "Sun":
                    body.trajectory.append(
                        body.CelesPosition.copy()
                    )
                    body.trajectoryTimes.append(
                        referenceTime
                    )
                continue

            state = jplEphemeris.getState(
                body.CelesName,
                point
            )

            body.setPosition(
                state["position"]
            )

            body.CelesVelocity = (
                state["velocity"]
            )

            body.trajectory.append(
                body.CelesPosition.copy()
            )

            body.trajectoryTimes.append(
                state["time"]
            )