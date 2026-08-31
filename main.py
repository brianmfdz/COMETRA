print("COMETRA is starting...")

from celestial_body import CelestialBody, Planet, Comet
from solar_system import SolarSystem
from physics_model import PhysicsModel

physicsModel = PhysicsModel()
physicsModel.showModelInfo()

sun = Planet("Sun", (0, 0, 0))

earth = Planet("Earth", (0, 0, 0))

Jupiter = Planet("Jupiter", (3, 4, 5), (0, 29.78, 0))


comet1 = Comet("46p", (1, 2, 3), "C-2024")
comet2 = Comet("67p", (4, 5, 6), "C-2025", (0, 20, 0))

bodies = [sun, earth, Jupiter, comet1, comet2]

solarSystem = SolarSystem(bodies)

solarSystem.bodies[0].showInfo()

solarSystem.bodies[0].setPosition((2, 0, 0))

solarSystem.bodies[0].showInfo()

print("All celestial bodies information:")

solarSystem.showInfo()