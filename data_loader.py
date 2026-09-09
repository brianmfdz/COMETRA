import requests
import re
from datetime import datetime, timedelta

from celestial_body import Planet, Comet


class DataLoader:

    API_URL = (
        "https://ssd.jpl.nasa.gov/api/horizons.api"
    )

    CHUNK_YEARS = 5


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
            "VEC_TABLE": "'2'",
            "VEC_LABELS": "'YES'"
        }


        response = requests.get(
            self.API_URL,
            params=parameters,
            timeout=60
        )


        response.raise_for_status()


        data = response.json()


        if "result" not in data:

            message = data.get(
                "message",
                "Unknown JPL error."
            )

            raise ValueError(
                f"JPL request failed for "
                f"body '{bodyID}'. "
                f"JPL message: {message}"
            )


        result = data["result"]


        if (
            "$$SOE" not in result
            or "$$EOE" not in result
        ):

            raise ValueError(
                f"JPL returned no ephemeris data "
                f"for body '{bodyID}' "
                f"from {startDate} to {endDate}. "
                f"JPL response: "
                f"{result[:500]}"
            )


        return data


    def parseEphemeris(
        self,
        data,
        startDate=None,
        stepSize=None
    ):

        result = data["result"]


        start = result.find(
            "$$SOE"
        )


        end = result.find(
            "$$EOE"
        )


        if start == -1 or end == -1:

            raise ValueError(
                "Ephemeris data not found."
            )


        stateData = result[
            start + len("$$SOE"):
            end
        ]


        pattern = re.compile(
            r"""
            (?P<time>
                \d{4}
                -
                [A-Za-z]{3}
                -
                \d{2}
                \s+
                \d{2}
                :
                \d{2}
                :
                \d{2}
                (?:\.\d+)?
            )

            .*?

            X\s*=\s*
            (?P<x>
                [+-]?
                \d+(?:\.\d+)?
                (?:E[+-]?\d+)?
            )

            .*?

            Y\s*=\s*
            (?P<y>
                [+-]?
                \d+(?:\.\d+)?
                (?:E[+-]?\d+)?
            )

            .*?

            Z\s*=\s*
            (?P<z>
                [+-]?
                \d+(?:\.\d+)?
                (?:E[+-]?\d+)?
            )

            .*?

            VX\s*=\s*
            (?P<vx>
                [+-]?
                \d+(?:\.\d+)?
                (?:E[+-]?\d+)?
            )

            .*?

            VY\s*=\s*
            (?P<vy>
                [+-]?
                \d+(?:\.\d+)?
                (?:E[+-]?\d+)?
            )

            .*?

            VZ\s*=\s*
            (?P<vz>
                [+-]?
                \d+(?:\.\d+)?
                (?:E[+-]?\d+)?
            )
            """,
            re.VERBOSE
            | re.DOTALL
        )


        matches = list(
            pattern.finditer(
                stateData
            )
        )


        if len(matches) == 0:

            raise ValueError(
                "No state vectors were found "
                "in the JPL response."
            )


        ephemeris = []


        for match in matches:

            timeText = match.group(
                "time"
            )


            timeText = (
                timeText.split(".")[0]
            )


            timestamp = datetime.strptime(
                timeText,
                "%Y-%b-%d %H:%M:%S"
            )


            position = [

                float(
                    match.group("x")
                ) * 1000,

                float(
                    match.group("y")
                ) * 1000,

                float(
                    match.group("z")
                ) * 1000
            ]


            velocity = [

                float(
                    match.group("vx")
                ) * 1000,

                float(
                    match.group("vy")
                ) * 1000,

                float(
                    match.group("vz")
                ) * 1000
            ]


            ephemeris.append(
                {
                    "time": timestamp,
                    "position": position,
                    "velocity": velocity
                }
            )


        return ephemeris


    def createChunks(
        self,
        startDate,
        endDate
    ):

        chunks = []

        currentStart = startDate


        while currentStart < endDate:

            try:

                currentEnd = currentStart.replace(
                    year=currentStart.year
                    + self.CHUNK_YEARS
                )

            except ValueError:

                currentEnd = (
                    currentStart
                    + timedelta(
                        days=365
                        * self.CHUNK_YEARS
                    )
                )


            if currentEnd > endDate:

                currentEnd = endDate


            chunks.append(
                (
                    currentStart,
                    currentEnd
                )
            )


            if currentEnd >= endDate:

                break


            currentStart = currentEnd


        return chunks


    def loadEphemeris(
        self,
        bodyName,
        bodyID,
        startDate,
        endDate,
        stepSize
    ):

        startDateTime = datetime.strptime(
            startDate,
            "%Y-%m-%d %H:%M"
        )


        endDateTime = datetime.strptime(
            endDate,
            "%Y-%m-%d %H:%M"
        )


        chunks = self.createChunks(
            startDateTime,
            endDateTime
        )


        completeEphemeris = []


        for chunkStart, chunkEnd in chunks:

            chunkStartText = (
                chunkStart.strftime(
                    "%Y-%m-%d %H:%M"
                )
            )


            chunkEndText = (
                chunkEnd.strftime(
                    "%Y-%m-%d %H:%M"
                )
            )


            try:

                data = self.getEphemeris(
                    bodyID,
                    chunkStartText,
                    chunkEndText,
                    stepSize
                )


                chunkEphemeris = (
                    self.parseEphemeris(
                        data,
                        chunkStartText,
                        stepSize
                    )
                )


            except Exception as error:

                raise ValueError(
                    f"Failed loading "
                    f"{bodyName} "
                    f"({bodyID}) "
                    f"for "
                    f"{chunkStartText} → "
                    f"{chunkEndText}. "
                    f"{error}"
                )


            if len(
                completeEphemeris
            ) > 0:

                lastTime = (
                    completeEphemeris[-1]["time"]
                )


                chunkEphemeris = [

                    state

                    for state in chunkEphemeris

                    if state["time"] > lastTime

                ]


            completeEphemeris.extend(
                chunkEphemeris
            )


        if len(
            completeEphemeris
        ) == 0:

            raise ValueError(
                f"No JPL ephemeris data was loaded "
                f"for {bodyName}."
            )


        return completeEphemeris


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