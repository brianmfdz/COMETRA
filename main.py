print("COMETRA is starting...")

from celestial_body import Planet
from solar_system import SolarSystem
from simulator import Simulator
from physics_model import PhysicsModel
from data_loader import DataLoader


physicsModel = PhysicsModel()
dataLoader = DataLoader()


sun = Planet(
    "Sun",
    (0, 0, 0),
    (0, 0, 0),
    physicsModel.SUN_MASS
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


planets = []

for name, bodyID, mass in planetData:

    planet = dataLoader.loadPlanet(
        name,
        bodyID,
        mass,
        "2026-09-02"
    )

    planets.append(planet)


bodies = [sun] + planets


solarSystem = SolarSystem(bodies)

simulator = Simulator(
    solarSystem,
    physicsModel
)


print("\nBefore simulation:")
solarSystem.showInfo()


timeStep = 60 * 60

for i in range(24):
    simulator.step(timeStep)


print("\nAfter 24 hours:")
solarSystem.showInfo()