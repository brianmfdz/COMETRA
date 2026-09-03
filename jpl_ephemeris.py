class JPLEphemeris:

    def __init__(self):
        self.bodyData = {}

    def addBody(
        self,
        bodyName,
        ephemeris
    ):

        self.bodyData[bodyName] = ephemeris

    def getState(
        self,
        bodyName,
        point
    ):

        return self.bodyData[
            bodyName
        ][point]

    def getBodyNames(self):

        return self.bodyData.keys()

    def getPointCount(
        self,
        bodyName
    ):

        return len(
            self.bodyData[bodyName]
        )