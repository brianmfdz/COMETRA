import numpy as np


class CelestialBody:
    def __init__(
        self,
        CelesName,
        CelesPosition,
        CelesVelocity=(0, 0, 0),
        CelesMass=0
    ):
        self.CelesName = CelesName
        self.CelesPosition = np.array(CelesPosition, dtype=float)
        self.CelesVelocity = np.array(CelesVelocity, dtype=float)
        self.CelesMass = CelesMass

        self.trajectory = [
            self.CelesPosition.copy()
        ]

    def setPosition(self, newPosition):
        self.CelesPosition = np.array(
            newPosition,
            dtype=float
        )


class Planet(CelestialBody):
    def __init__(
        self,
        CelesName,
        CelesPosition,
        CelesVelocity=(0, 0, 0),
        CelesMass=0
    ):
        super().__init__(
            CelesName,
            CelesPosition,
            CelesVelocity,
            CelesMass
        )

    def showInfo(self):
        print(
            f"Name: {self.CelesName}, "
            f"Position: {self.CelesPosition}, "
            f"Velocity: {self.CelesVelocity}, "
            f"Mass: {self.CelesMass}"
        )


class Comet(CelestialBody):
    def __init__(
        self,
        CelesName,
        CelesPosition,
        CometID,
        CelesVelocity=(0, 0, 0),
        CelesMass=0
    ):
        super().__init__(
            CelesName,
            CelesPosition,
            CelesVelocity,
            CelesMass
        )

        self.CometID = CometID

    def showInfo(self):
        print(
            f"Name: {self.CelesName}, "
            f"Position: {self.CelesPosition}, "
            f"Velocity: {self.CelesVelocity}, "
            f"Mass: {self.CelesMass}, "
            f"Comet ID: {self.CometID}"
        )


class CometFragment(Comet):
    def __init__(
        self,
        CelesName,
        CelesPosition,
        CometID,
        FragmentID,
        CelesVelocity=(0, 0, 0),
        CelesMass=0
    ):
        super().__init__(
            CelesName,
            CelesPosition,
            CometID,
            CelesVelocity,
            CelesMass
        )

        self.FragmentID = FragmentID

    def showInfo(self):
        print(
            f"Name: {self.CelesName}, "
            f"Fragment ID: {self.FragmentID}, "
            f"Position: {self.CelesPosition}, "
            f"Velocity: {self.CelesVelocity}"
        )