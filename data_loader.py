import requests
import re

from celestial_body import Planet, Comet


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

        start = result.find("$$SOE")
        end = result.find("$$EOE")

        if start == -1 or end == -1:
            raise ValueError("State vector data not found")

        stateData = result[start:end]

        x = re.search(
            r"X\s*=\s*([+-]?\d+(?:\.\d+)?(?:E[+-]?\d+)?)",
            stateData
        )

        y = re.search(
            r"Y\s*=\s*([+-]?\d+(?:\.\d+)?(?:E[+-]?\d+)?)",
            stateData
        )

        z = re.search(
            r"Z\s*=\s*([+-]?\d+(?:\.\d+)?(?:E[+-]?\d+)?)",
            stateData
        )

        vx = re.search(
            r"VX\s*=\s*([+-]?\d+(?:\.\d+)?(?:E[+-]?\d+)?)",
            stateData
        )

        vy = re.search(
            r"VY\s*=\s*([+-]?\d+(?:\.\d+)?(?:E[+-]?\d+)?)",
            stateData
        )

        vz = re.search(
            r"VZ\s*=\s*([+-]?\d+(?:\.\d+)?(?:E[+-]?\d+)?)",
            stateData
        )

        if not x or not y or not z:
            raise ValueError("Position data not found")

        if not vx or not vy or not vz:
            raise ValueError("Velocity data not found")

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

        data = self.getStateVector(
            bodyID,
            date
        )

        position, velocity = self.parseStateVector(data)

        planet = Planet(
            name,
            position,
            velocity,
            mass
        )

        return planet

    def loadComet(self, name, bodyID, cometID, date):

        data = self.getStateVector(
            bodyID,
            date
        )

        position, velocity = self.parseStateVector(data)

        comet = Comet(
            name,
            position,
            cometID,
            velocity
        )

        return comet