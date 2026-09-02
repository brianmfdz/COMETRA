import requests


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