import numpy as np

from celestial_body import CometFragment


class FragmentationModel:

    def createFragments(
        self,
        comet,
        separationVelocities
    ):
        fragments = []

        for i, separationVelocity in enumerate(
            separationVelocities
        ):

            fragmentID = f"F{i + 1}"

            fragmentName = (
                f"{comet.CelesName} - {fragmentID}"
            )

            fragmentVelocity = (
                comet.CelesVelocity
                + np.array(
                    separationVelocity,
                    dtype=float
                )
            )

            fragment = CometFragment(
                fragmentName,
                comet.CelesPosition.copy(),
                comet.CometID,
                fragmentID,
                fragmentVelocity
            )

            fragments.append(fragment)

        return fragments