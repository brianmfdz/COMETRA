print("COMETRA is starting...")

from simulation_config import SimulationConfig
from simulation_runner import SimulationRunner


config = SimulationConfig(
    "1P/Halley",
    "90000030;",
    "1P",
    "2026-09-02",
    24 * 60 * 60,
    60 * 60,
    12 * 60 * 60,
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
    "Number of fragments:",
    len(results["fragments"])
)


print("\nFragment results:")

for result in results["closestApproaches"]:

    fragment = result["fragment"]

    print(
        fragment.FragmentID,
        "trajectory points:",
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