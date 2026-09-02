print("COMETRA is starting...")

from celestial_body import Planet
from solar_system import SolarSystem
from simulator import Simulator
from physics_model import PhysicsModel
from data_loader import DataLoader


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

for i in range(24):
    simulator.step(timeStep)


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