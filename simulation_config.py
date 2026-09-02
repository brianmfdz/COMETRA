class SimulationConfig:

    def __init__(
        self,
        cometName,
        cometID,
        startDate,
        simulationDuration,
        timeStep,
        fragmentationTime,
        separationVelocities
    ):
        self.cometName = cometName
        self.cometID = cometID
        self.startDate = startDate
        self.simulationDuration = simulationDuration
        self.timeStep = timeStep
        self.fragmentationTime = fragmentationTime
        self.separationVelocities = separationVelocities