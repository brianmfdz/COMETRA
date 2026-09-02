class SimulationConfig:

    def __init__(
        self,
        cometName,
        cometID,
        cometDesignation,
        startDate,
        simulationDuration,
        timeStep,
        fragmentationTime,
        separationVelocities
    ):
        self.cometName = cometName
        self.cometID = cometID
        self.cometDesignation = cometDesignation
        self.startDate = startDate
        self.simulationDuration = simulationDuration
        self.timeStep = timeStep
        self.fragmentationTime = fragmentationTime
        self.separationVelocities = separationVelocities