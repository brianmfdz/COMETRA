class RealBodySimulator:

    def updateBodies(
        self,
        solarSystem,
        jplEphemeris,
        point
    ):

        for body in solarSystem.bodies:

            if body.CelesName not in (
                jplEphemeris.getBodyNames()
            ):
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