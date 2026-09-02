# print("COMETRA is starting...")

# from celestial_body import Planet, Comet
# from solar_system import SolarSystem
# from simulator import Simulator
# from physics_model import PhysicsModel


# physicsModel = PhysicsModel()
# physicsModel.showModelInfo()


# sun = Planet(
#     "Sun",
#     (0, 0, 0),
#     (0, 0, 0),
#     physicsModel.SUN_MASS
# )

# mercury = Planet(
#     "Mercury",
#     (5.790e10, 0, 0),
#     (0, 47360, 0),
#     3.301e23
# )

# venus = Planet(
#     "Venus",
#     (1.082e11, 0, 0),
#     (0, 35020, 0),
#     4.867e24
# )

# earth = Planet(
#     "Earth",
#     (1.496e11, 0, 0),
#     (0, 29780, 0),
#     5.972e24
# )

# mars = Planet(
#     "Mars",
#     (2.279e11, 0, 0),
#     (0, 24130, 0),
#     6.417e23
# )

# jupiter = Planet(
#     "Jupiter",
#     (7.785e11, 0, 0),
#     (0, 13070, 0),
#     1.898e27
# )

# saturn = Planet(
#     "Saturn",
#     (1.434e12, 0, 0),
#     (0, 9680, 0),
#     5.683e26
# )

# uranus = Planet(
#     "Uranus",
#     (2.871e12, 0, 0),
#     (0, 6800, 0),
#     8.681e25
# )

# neptune = Planet(
#     "Neptune",
#     (4.495e12, 0, 0),
#     (0, 5430, 0),
#     1.024e26
# )


# bodies = [
#     sun,
#     mercury,
#     venus,
#     earth,
#     mars,
#     jupiter,
#     saturn,
#     uranus,
#     neptune
# ]


# solarSystem = SolarSystem(bodies)

# simulator = Simulator(solarSystem, physicsModel)


# print("\nBefore simulation:")
# solarSystem.showInfo()


# secondsInYear = 365 * 24 * 60 * 60
# timeStep = 60 * 60

# numberOfSteps = secondsInYear // timeStep

# for i in range(numberOfSteps):
#     simulator.step(timeStep)

# print("\nAfter 1 year:")
# solarSystem.showInfo()

print("Testing JPL API...")

from data_loader import DataLoader


dataLoader = DataLoader()

data = dataLoader.getStateVector(
    "399",
    "2026-09-02"
)

position, velocity = dataLoader.parseStateVector(data)

print("\nEarth position (m):")
print(position)

print("\nEarth velocity (m/s):")
print(velocity)