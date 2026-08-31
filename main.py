print("COMETRA is starting...")

from celestial_body import Planet, Comet
from solar_system import SolarSystem
from simulator import Simulator
from physics_model import PhysicsModel


physicsModel = PhysicsModel()
physicsModel.showModelInfo()


sun = Planet("Sun", (0, 0, 0))

earth = Planet("Earth", (0, 0, 0))

jupiter = Planet(
    "Jupiter",
    (3, 4, 5),
    (0, 29.78, 0)
)

comet1 = Comet(
    "46P",
    (1, 2, 3),
    "C-2024"
)

comet2 = Comet(
    "67P",
    (4, 5, 6),
    "C-2025",
    (0, 20, 0)
)


bodies = [sun, earth, jupiter, comet1, comet2]

solarSystem = SolarSystem(bodies)

simulator = Simulator(solarSystem)


print("\nBefore simulation:")
jupiter.showInfo()


simulator.step(1)


print("\nAfter 1 time step:")
jupiter.showInfo()


print("\nAll celestial bodies:")
solarSystem.showInfo()