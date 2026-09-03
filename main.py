print("COMETRA is starting...")

from simulation_config import SimulationConfig
from simulation_runner import SimulationRunner


config = SimulationConfig(
    "1P/Halley",
    "90000030;",
    "1P",
    "2026-09-02 12:00",
    "2026-09-03 12:00",
    [
        (10, 0, 0),
        (-10, 0, 0),
        (0, 10, 0),
        (0, -10, 0)
    ]
)


runner = SimulationRunner()

results = runner.run(config)


print("\nSimulation complete.")

print(
    "Comet:",
    results["comet"].CelesName
)

print(
    "Automatic simulation start:",
    results["simulationStartDate"]
)

print(
    "Fragmentation:",
    results["fragmentationDate"]
)

print(
    "Simulation end:",
    results["simulationEndDate"]
)

print(
    "JPL step:",
    results["jplStep"]
)

print(
    "Physics timestep:",
    results["timeStep"],
    "seconds"
)

print(
    "Number of fragments:",
    len(results["fragments"])
)


print("\nFragment results:")

for result in results["closestApproaches"]:

    fragment = result["fragment"]

    print(
        "\n",
        fragment.FragmentID
    )

    print(
        "Trajectory points:",
        len(fragment.trajectory)
    )

    print(
        "Closest Earth distance:",
        result["distance"] / 1000,
        "km"
    )

    print(
        "Closest trajectory point:",
        result["point"]
    )

    print(
        "Closest approach time:",
        result["time"]
    )


print("\nTimestamp verification:")

cometName = results["comet"].CelesName

firstTime = runner.jplEphemeris.getState(
    cometName,
    0
)["time"]

fragmentationPoint = results["fragmentationPoint"]

fragmentationTime = runner.jplEphemeris.getState(
    cometName,
    fragmentationPoint
)["time"]

lastPoint = (
    runner.jplEphemeris.getPointCount(
        cometName
    )
    - 1
)

lastTime = runner.jplEphemeris.getState(
    cometName,
    lastPoint
)["time"]

print(
    "First JPL time:",
    firstTime
)

print(
    "Fragmentation JPL time:",
    fragmentationTime
)

print(
    "Last JPL time:",
    lastTime
)