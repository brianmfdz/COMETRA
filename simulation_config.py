class SimulationConfig:

    def __init__(
        self,
        cometName,
        cometID,
        cometDesignation,
        fragmentationDate,
        simulationEndDate,
        separationVelocities
    ):
        self.cometName = cometName
        self.cometID = cometID
        self.cometDesignation = cometDesignation

        self.fragmentationDate = fragmentationDate
        self.simulationEndDate = simulationEndDate

        self.separationVelocities = separationVelocities