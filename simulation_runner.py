from datetime import datetime, timedelta

from celestial_body import Planet
from solar_system import SolarSystem
from physics_model import PhysicsModel
from data_loader import DataLoader
from fragmentation_model import FragmentationModel
from fragmentation_event import FragmentationEvent
from trajectory_analysis import TrajectoryAnalysis
from jpl_ephemeris import JPLEphemeris
from real_body_simulator import RealBodySimulator
from fragment_simulator import FragmentSimulator


class SimulationRunner:

    def __init__(self):

        self.physicsModel = PhysicsModel()

        self.dataLoader = DataLoader()

        self.fragmentationModel = (
            FragmentationModel()
        )

        self.trajectoryAnalysis = (
            TrajectoryAnalysis()
        )

        self.jplEphemeris = JPLEphemeris()

        self.realBodySimulator = (
            RealBodySimulator()
        )

        self.fragmentSimulator = (
            FragmentSimulator()
        )

    def createSun(self):

        return Planet(
            "Sun",
            (0, 0, 0),
            (0, 0, 0),
            self.physicsModel.SUN_MASS
        )

    def chooseJPLStep(
        self,
        startDate,
        endDate
    ):

        duration = (
            endDate - startDate
        )

        days = (
            duration.total_seconds()
            / 86400
        )

        if days <= 30:
            return "1h"

        if days <= 365:
            return "6h"

        return "1d"

    def loadBody(
        self,
        name,
        bodyID,
        mass,
        startDate,
        endDate,
        jplStep
    ):

        ephemeris = (
            self.dataLoader.loadEphemeris(
                name,
                bodyID,
                startDate.strftime(
                    "%Y-%m-%d %H:%M"
                ),
                endDate.strftime(
                    "%Y-%m-%d %H:%M"
                ),
                jplStep
            )
        )

        self.jplEphemeris.addBody(
            name,
            ephemeris
        )

        firstState = ephemeris[0]

        body = Planet(
            name,
            firstState["position"],
            firstState["velocity"],
            mass
        )

        return body

    def loadComet(
        self,
        config,
        startDate,
        endDate,
        jplStep
    ):

        ephemeris = (
            self.dataLoader.loadEphemeris(
                config.cometName,
                config.cometID,
                startDate.strftime(
                    "%Y-%m-%d %H:%M"
                ),
                endDate.strftime(
                    "%Y-%m-%d %H:%M"
                ),
                jplStep
            )
        )

        self.jplEphemeris.addBody(
            config.cometName,
            ephemeris
        )

        firstState = ephemeris[0]

        comet = self.dataLoader.loadComet(
            config.cometName,
            config.cometDesignation,
            firstState["position"],
            firstState["velocity"]
        )

        return comet

    def createFragmentationEvent(
        self,
        config
    ):

        fragmentationDate = datetime.strptime(
            config.fragmentationDate,
            "%Y-%m-%d %H:%M"
        )

        return FragmentationEvent(
            fragmentationDate,
            config.separationVelocities
        )

    def findEarth(
        self,
        solarSystem
    ):

        for body in solarSystem.bodies:

            if body.CelesName == "Earth":
                return body

        return None

    def getTimeStep(
        self,
        jplStep
    ):

        if jplStep == "1h":
            return 60 * 60

        if jplStep == "6h":
            return 6 * 60 * 60

        return 24 * 60 * 60

    def calculateFragmentationPoint(
        self,
        startDate,
        fragmentationDate,
        timeStep
    ):

        seconds = (
            fragmentationDate
            - startDate
        ).total_seconds()

        return int(
            seconds / timeStep
        )

    def run(
        self,
        config
    ):

        fragmentationDate = datetime.strptime(
            config.fragmentationDate,
            "%Y-%m-%d %H:%M"
        )

        simulationEndDate = datetime.strptime(
            config.simulationEndDate,
            "%Y-%m-%d %H:%M"
        )

        if simulationEndDate <= fragmentationDate:
            raise ValueError(
                "Simulation end date must be after "
                "the fragmentation date."
            )

        simulationStartDate = (
            fragmentationDate
            - timedelta(days=1)
        )

        jplStep = self.chooseJPLStep(
            simulationStartDate,
            simulationEndDate
        )

        timeStep = self.getTimeStep(
            jplStep
        )

        planetData = [
            ("Mercury", "199", 3.301e23),
            ("Venus", "299", 4.867e24),
            ("Earth", "399", 5.972e24),
            ("Mars", "499", 6.417e23),
            ("Jupiter", "599", 1.898e27),
            ("Saturn", "699", 5.683e26),
            ("Uranus", "799", 8.681e25),
            ("Neptune", "899", 1.024e26)
        ]

        sun = self.createSun()

        planets = []

        for name, bodyID, mass in planetData:

            planet = self.loadBody(
                name,
                bodyID,
                mass,
                simulationStartDate,
                simulationEndDate,
                jplStep
            )

            planets.append(planet)

        comet = self.loadComet(
            config,
            simulationStartDate,
            simulationEndDate,
            jplStep
        )

        bodies = (
            [sun]
            + planets
            + [comet]
        )

        solarSystem = SolarSystem(
            bodies
        )

        for body in solarSystem.bodies:

            body.trajectoryTimes = [
                simulationStartDate
            ]

        fragmentationEvent = (
            self.createFragmentationEvent(
                config
            )
        )

        totalPoints = (
            self.jplEphemeris.getPointCount(
                config.cometName
            )
        )

        fragmentationPoint = (
            self.calculateFragmentationPoint(
                simulationStartDate,
                fragmentationDate,
                timeStep
            )
        )

        if fragmentationPoint >= totalPoints:

            raise ValueError(
                "Fragmentation point is outside "
                "the available JPL data."
            )

        for point in range(
            1,
            fragmentationPoint + 1
        ):

            self.realBodySimulator.updateBodies(
                solarSystem,
                self.jplEphemeris,
                point
            )

        cometState = (
            self.jplEphemeris.getState(
                config.cometName,
                fragmentationPoint
            )
        )

        comet.setPosition(
            cometState["position"]
        )

        comet.CelesVelocity = (
            cometState["velocity"]
        )

        fragments = (
            self.fragmentationModel.createFragments(
                comet,
                fragmentationEvent.separationVelocities
            )
        )

        for fragment in fragments:

            fragment.trajectoryTimes = [
                fragmentationDate
            ]

            solarSystem.bodies.append(
                fragment
            )

        for point in range(
            fragmentationPoint + 1,
            totalPoints
        ):

            self.realBodySimulator.updateBodies(
                solarSystem,
                self.jplEphemeris,
                point
            )

            newTime = (
                self.jplEphemeris.getState(
                    config.cometName,
                    point
                )["time"]
            )

            for fragment in fragments:

                self.fragmentSimulator.step(
                    fragment,
                    solarSystem,
                    timeStep,
                    newTime
                )

        earth = self.findEarth(
            solarSystem
        )

        closestApproaches = []

        if earth is not None:

            for fragment in fragments:

                (
                    minimumDistance,
                    closestPoint,
                    closestTime
                ) = (
                    self.trajectoryAnalysis
                    .calculateClosestApproach(
                        earth,
                        fragment
                    )
                )

                closestApproaches.append(
                    {
                        "fragment": fragment,
                        "distance": minimumDistance,
                        "point": closestPoint,
                        "time": closestTime
                    }
                )

        return {
            "solarSystem": solarSystem,
            "comet": comet,
            "fragments": fragments,
            "closestApproaches": closestApproaches,
            "simulationStartDate": simulationStartDate,
            "fragmentationDate": fragmentationDate,
            "simulationEndDate": simulationEndDate,
            "jplStep": jplStep,
            "timeStep": timeStep,
            "fragmentationPoint": fragmentationPoint
        }