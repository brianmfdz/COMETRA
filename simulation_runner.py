from celestial_body import Planet
from simulator import Simulator
from solar_system import SolarSystem
from physics_model import PhysicsModel
from data_loader import DataLoader
from fragmentation_model import FragmentationModel
from fragmentation_event import FragmentationEvent
from trajectory_analysis import TrajectoryAnalysis


class SimulationRunner:

    def __init__(self):

        self.physicsModel = PhysicsModel()
        self.dataLoader = DataLoader()
        self.fragmentationModel = FragmentationModel()
        self.trajectoryAnalysis = TrajectoryAnalysis()

    def createSun(self):

        return Planet(
            "Sun",
            (0, 0, 0),
            (0, 0, 0),
            self.physicsModel.SUN_MASS
        )

    def loadPlanets(self, date):

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

        planets = []

        for name, bodyID, mass in planetData:

            planet = self.dataLoader.loadPlanet(
                name,
                bodyID,
                mass,
                date
            )

            planets.append(planet)

        return planets

    def findEarth(self, solarSystem):

        for body in solarSystem.bodies:

            if body.CelesName == "Earth":
                return body

        return None

    def run(self, config):

        sun = self.createSun()

        planets = self.loadPlanets(
            config.startDate
        )

        comet = self.dataLoader.loadComet(
            config.cometName,
            config.cometID,
            config.cometDesignation,
            config.startDate
        )

        bodies = [sun] + planets + [comet]

        solarSystem = SolarSystem(bodies)

        simulator = Simulator(
            solarSystem,
            self.physicsModel
        )

        fragmentationEvent = FragmentationEvent(
            config.fragmentationTime,
            config.separationVelocities
        )

        fragments = simulator.simulateWithFragmentation(
            comet,
            fragmentationEvent,
            self.fragmentationModel,
            config.simulationDuration,
            config.timeStep
        )

        earth = self.findEarth(
            solarSystem
        )

        closestApproaches = []

        for fragment in fragments:

            minimumDistance, closestPoint = (
                self.trajectoryAnalysis.calculateClosestApproach(
                    earth,
                    fragment
                )
            )

            closestApproaches.append(
                {
                    "fragment": fragment,
                    "distance": minimumDistance,
                    "point": closestPoint
                }
            )

        return {
            "solarSystem": solarSystem,
            "comet": comet,
            "fragments": fragments,
            "closestApproaches": closestApproaches
        }