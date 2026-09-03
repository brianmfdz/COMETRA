import requests
import re
from datetime import datetime, timedelta

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

    def parseEphemeris(
        self,
        data,
        startDate,
        stepSize
    ):

        result = data["result"]

        start = result.find("$$SOE")
        end = result.find("$$EOE")

        if start == -1 or end == -1:
            raise ValueError(
                "Ephemeris data not found."
            )

        stateData = result[start:end]

        xValues = re.findall(
            r"X\s*=\s*([+-]?\d+(?:\.\d+)?(?:E[+-]?\d+)?)",
            stateData
        )

        yValues = re.findall(
            r"Y\s*=\s*([+-]?\d+(?:\.\d+)?(?:E[+-]?\d+)?)",
            stateData
        )

        zValues = re.findall(
            r"Z\s*=\s*([+-]?\d+(?:\.\d+)?(?:E[+-]?\d+)?)",
            stateData
        )

        vxValues = re.findall(
            r"VX\s*=\s*([+-]?\d+(?:\.\d+)?(?:E[+-]?\d+)?)",
            stateData
        )

        vyValues = re.findall(
            r"VY\s*=\s*([+-]?\d+(?:\.\d+)?(?:E[+-]?\d+)?)",
            stateData
        )

        vzValues = re.findall(
            r"VZ\s*=\s*([+-]?\d+(?:\.\d+)?(?:E[+-]?\d+)?)",
            stateData
        )

        pointCount = min(
            len(xValues),
            len(yValues),
            len(zValues),
            len(vxValues),
            len(vyValues),
            len(vzValues)
        )

        if pointCount == 0:
            raise ValueError(
                "No state vectors were found."
            )

        startDateTime = datetime.strptime(
            startDate,
            "%Y-%m-%d %H:%M"
        )

        if stepSize == "1h":
            timeStep = timedelta(hours=1)

        elif stepSize == "6h":
            timeStep = timedelta(hours=6)

        elif stepSize == "1d":
            timeStep = timedelta(days=1)

        else:
            raise ValueError(
                f"Unsupported JPL step size: {stepSize}"
            )

        ephemeris = []

        for i in range(pointCount):

            timestamp = (
                startDateTime
                + i * timeStep
            )

            position = [
                float(xValues[i]) * 1000,
                float(yValues[i]) * 1000,
                float(zValues[i]) * 1000
            ]

            velocity = [
                float(vxValues[i]) * 1000,
                float(vyValues[i]) * 1000,
                float(vzValues[i]) * 1000
            ]

            ephemeris.append(
                {
                    "time": timestamp,
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

        return self.parseEphemeris(
            data,
            startDate,
            stepSize
        )

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