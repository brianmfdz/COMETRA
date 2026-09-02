class FragmentationEvent:
    def __init__(
        self,
        fragmentationTime,
        separationVelocities
    ):
        self.fragmentationTime = fragmentationTime
        self.separationVelocities = separationVelocities

    def isTime(self, currentTime):
        return currentTime >= self.fragmentationTime

    def getFragmentCount(self):
        return len(self.separationVelocities)