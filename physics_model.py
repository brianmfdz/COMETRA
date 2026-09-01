import numpy as np


class PhysicsModel:
    G = 6.67430e-11
    SUN_MASS = 1.989e30

    def showModelInfo(self):
        print("physics_model_info : Gravitational Model")

    def calculateSunGravity(self, position):
        distance = np.linalg.norm(position)

        acceleration = -self.G * self.SUN_MASS * position / distance**3

        return acceleration