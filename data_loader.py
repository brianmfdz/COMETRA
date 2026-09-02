import requests
import re
from celestial_body import Planet

class DataLoader:

    API_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"

    def getStateVector(self, bodyID, date):

        parameters = {
            "format": "json",
            "COMMAND": f"'{bodyID}'",
            "EPHEM_TYPE": "'VECTORS'",
            "CENTER": "'500@10'",
            "START_TIME": f"'{date}'",
            "STOP_TIME": f"'{date} 00:01'",
            "STEP_SIZE": "'1d'",
            "OUT_UNITS": "'KM-S'",
            "REF_PLANE": "'ECLIPTIC'",
            "REF_SYSTEM": "'ICRF'",
            "VEC_TABLE": "'2'"
        }

        response = requests.get(
            self.API_URL,
            params=parameters
        )

        response.raise_for_status()

        data = response.json()

        return data

    def parseStateVector(self, data):

        result = data["result"]

        x = re.search(r"X\s*=\s*([+-]?\d+\.?\d*E?[+-]?\d*)", result)
        y = re.search(r"Y\s*=\s*([+-]?\d+\.?\d*E?[+-]?\d*)", result)
        z = re.search(r"Z\s*=\s*([+-]?\d+\.?\d*E?[+-]?\d*)", result)

        vx = re.search(r"VX=\s*([+-]?\d+\.?\d*E?[+-]?\d*)", result)
        vy = re.search(r"VY=\s*([+-]?\d+\.?\d*E?[+-]?\d*)", result)
        vz = re.search(r"VZ=\s*([+-]?\d+\.?\d*E?[+-]?\d*)", result)

        position = [
            float(x.group(1)) * 1000,
            float(y.group(1)) * 1000,
            float(z.group(1)) * 1000
        ]

        velocity = [
            float(vx.group(1)) * 1000,
            float(vy.group(1)) * 1000,
            float(vz.group(1)) * 1000
        ]

        return position, velocity

    def loadPlanet(self, name, bodyID, mass, date):

        data = self.getStateVector(bodyID, date)

        position, velocity = self.parseStateVector(data)

        planet = Planet(
            name,
            position,
            velocity,
            mass
        )

        return planet