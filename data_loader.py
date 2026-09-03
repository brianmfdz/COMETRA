import requests
import re

from celestial_body import Planet, Comet


class DataLoader:

    API_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"

    def getEphemeris(
        self,
        bodyID,
        startDate,
        endDate,
        stepSize
    ):

        parameters = {
            "format": "json",
            "COMMAND": f"'{bodyID}'",
            "EPHEM_TYPE": "'VECTORS'",
            "CENTER": "'500@10'",
            "START_TIME": f"'{startDate}'",
            "STOP_TIME": f"'{endDate}'",
            "STEP_SIZE": f"'{stepSize}'",
            "OUT_UNITS": "'KM-S'",
            "REF_PLANE": "'ECLIPTIC'",
            "REF_SYSTEM": "'ICRF'",
            "VEC_TABLE": "'2'"
        }

        response = requests.get(
            self.API_URL,
            params=parameters,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        if "result" not in data:
            raise ValueError(
                "JPL Horizons did not return a result."
            )

        return data

    def parseEphemeris(self, data):

        result = data["result"]

        start = result.find("$$SOE")
        end = result.find("$$EOE")

        if start == -1 or end == -1:
            raise ValueError(
                "Ephemeris data not found."
            )

        stateData = result[start:end]

        pattern = (
            r"X\s*=\s*([+-]?\d+(?:\.\d+)?(?:E[+-]?\d+)?)"
            r"\s*Y\s*=\s*([+-]?\d+(?:\.\d+)?(?:E[+-]?\d+)?)"
            r"\s*Z\s*=\s*([+-]?\d+(?:\.\d+)?(?:E[+-]?\d+)?)"
            r"\s*VX\s*=\s*([+-]?\d+(?:\.\d+)?(?:E[+-]?\d+)?)"
            r"\s*VY\s*=\s*([+-]?\d+(?:\.\d+)?(?:E[+-]?\d+)?)"
            r"\s*VZ\s*=\s*([+-]?\d+(?:\.\d+)?(?:E[+-]?\d+)?)"
        )

        matches = re.findall(
            pattern,
            stateData
        )

        if not matches:
            raise ValueError(
                "No state vectors were found."
            )

        ephemeris = []

        for match in matches:

            x, y, z, vx, vy, vz = match

            position = [
                float(x) * 1000,
                float(y) * 1000,
                float(z) * 1000
            ]

            velocity = [
                float(vx) * 1000,
                float(vy) * 1000,
                float(vz) * 1000
            ]

            ephemeris.append(
                {
                    "position": position,
                    "velocity": velocity
                }
            )

        return ephemeris

    def loadEphemeris(
        self,
        bodyName,
        bodyID,
        startDate,
        endDate,
        stepSize
    ):

        data = self.getEphemeris(
            bodyID,
            startDate,
            endDate,
            stepSize
        )

        return self.parseEphemeris(data)

    def loadPlanet(
        self,
        name,
        bodyID,
        mass,
        position,
        velocity
    ):

        return Planet(
            name,
            position,
            velocity,
            mass
        )

    def loadComet(
        self,
        name,
        cometID,
        position,
        velocity
    ):

        return Comet(
            name,
            position,
            cometID,
            velocity
        )