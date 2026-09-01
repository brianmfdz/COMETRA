import numpy as np


class PhysicsModel:
    G = 6.67430e-11
    SUN_MASS = 1.989e30

    def showModelInfo(self):
        print("physics_model_info : Gravitational Model")

    def calculateGravity(self, sourceBody, targetPosition):
        direction = sourceBody.CelesPosition - targetPosition
        distance = np.linalg.norm(direction)

        acceleration = (
            self.G
            * sourceBody.CelesMass
            * direction
            / distance**3
        )

        return acceleration