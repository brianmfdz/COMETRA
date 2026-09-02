print("COMETRA is starting...")

from celestial_body import Planet, CometFragment
from solar_system import SolarSystem
from simulator import Simulator
from physics_model import PhysicsModel
from data_loader import DataLoader
from fragmentation_model import FragmentationModel
from fragmentation_event import FragmentationEvent
from trajectory_analysis import TrajectoryAnalysis

physicsModel = PhysicsModel()
dataLoader = DataLoader()


# Sun

sun = Planet(
    "Sun",
    (0, 0, 0),
    (0, 0, 0),
    physicsModel.SUN_MASS
)


# Planets

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

    planet = dataLoader.loadPlanet(
        name,
        bodyID,
        mass,
        "2026-09-02"
    )

    planets.append(planet)


# Comet

halley = dataLoader.loadComet(
    "1P/Halley",
    "90000030;",
    "1P",
    "2026-09-02"
)


# Solar System

bodies = [sun] + planets + [halley]

solarSystem = SolarSystem(bodies)

simulator = Simulator(
    solarSystem,
    physicsModel
)


print("\nBefore simulation:")
solarSystem.showInfo()


# Simulate 24 hours

timeStep = 60 * 60
simulationTime = 24 * 60 * 60

simulator.simulate(
    simulationTime,
    timeStep
)


print("\nAfter 24 hours:")
solarSystem.showInfo()

print("\nTrajectory test:")

print(
    "Halley trajectory points:",
    len(halley.trajectory)
)

print(
    "First position:",
    halley.trajectory[0]
)

print(
    "Last position:",
    halley.trajectory[-1]
)

print("\nFragment object test:")

testFragment = CometFragment(
    "Halley Fragment 1",
    halley.CelesPosition.copy(),
    halley.CometID,
    "F1",
    halley.CelesVelocity.copy()
)

testFragment.showInfo()

print("\nFragmentation simulation test:")

fragmentationModel = FragmentationModel()

separationVelocities = [
    (10, 0, 0),
    (-10, 0, 0),
    (0, 10, 0)
]

fragments = fragmentationModel.createFragments(
    halley,
    separationVelocities
)

for fragment in fragments:
    solarSystem.bodies.append(fragment)


print("\nFragments before simulation:")

for fragment in fragments:
    fragment.showInfo()


# Simulate the fragments for 24 hours

for i in range(24):
    simulator.step(timeStep)


print("\nFragments after simulation:")

for fragment in fragments:
    fragment.showInfo()


print("\nFragment trajectories:")

for fragment in fragments:
    print(
        fragment.FragmentID,
        "trajectory points:",
        len(fragment.trajectory)
    )

    print("\nFinal fragment positions:")

for fragment in fragments:
    print(
        fragment.FragmentID,
        fragment.CelesPosition
    )

print("\nFragmentation event test:")

fragmentationEvent = FragmentationEvent(
    12 * timeStep,
    [
        (10, 0, 0),
        (-10, 0, 0),
        (0, 10, 0)
    ]
)

print(
    "Fragmentation time:",
    fragmentationEvent.fragmentationTime
)

print(
    "Current simulation time:",
    simulator.currentTime
)

print(
    "Event reached:",
    fragmentationEvent.isTime(
        simulator.currentTime
    )
)

print("\nSimulation event timing test:")

eventTime = simulator.currentTime + (12 * timeStep)

print(
    "Current time before event:",
    simulator.currentTime
)

simulator.simulateUntil(
    eventTime,
    timeStep
)

print(
    "Current time after event:",
    simulator.currentTime
)

print(
    "Target event time:",
    eventTime
)

print("\nConfigurable fragmentation simulation test:")

# Create a new comet simulation

testHalley = dataLoader.loadComet(
    "1P/Halley",
    "90000030;",
    "1P",
    "2026-09-02"
)

testBodies = [sun] + planets + [testHalley]

testSolarSystem = SolarSystem(testBodies)

testSimulator = Simulator(
    testSolarSystem,
    physicsModel
)

testFragmentationModel = FragmentationModel()


# Fragmentation configuration

fragmentationTime = 12 * timeStep

separationVelocities = [
    (10, 0, 0),
    (-10, 0, 0),
    (0, 10, 0),
    (0, -10, 0)
]


testFragmentationEvent = FragmentationEvent(
    fragmentationTime,
    separationVelocities
)


# Run simulation

endTime = 24 * timeStep

testFragments = testSimulator.simulateWithFragmentation(
    testHalley,
    testFragmentationEvent,
    testFragmentationModel,
    endTime,
    timeStep
)


print(
    "Fragmentation time:",
    fragmentationTime
)

print(
    "Simulation end time:",
    testSimulator.currentTime
)

print(
    "Number of fragments:",
    testFragmentationEvent.getFragmentCount()
)


for fragment in testFragments:

    print(
        fragment.FragmentID,
        "separation velocity:",
        fragment.CelesVelocity
    )

    print(
        fragment.FragmentID,
        "trajectory points:",
        len(fragment.trajectory)
    )

print("\nClosest approach analysis test:")

trajectoryAnalysis = TrajectoryAnalysis()

earth = None

for body in testSolarSystem.bodies:

    if body.CelesName == "Earth":
        earth = body
        break


for fragment in testFragments:

    minimumDistance, closestPoint = (
        trajectoryAnalysis.calculateClosestApproach(
            earth,
            fragment
        )
    )

    print(
        fragment.FragmentID,
        "closest Earth distance:",
        minimumDistance / 1000,
        "km"
    )

    print(
        fragment.FragmentID,
        "closest trajectory point:",
        closestPoint
    )