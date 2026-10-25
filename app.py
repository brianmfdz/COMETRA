from bisect import bisect_left

import streamlit as st
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, date, time

from simulation_runner import SimulationRunner
from simulation_config import SimulationConfig
from playback_view import createPlaybackHtml, getCollisionFrameIndex


PLANET_COLORS = {
    "Mercury": "#697586",
    "Venus": "#C77700",
    "Earth": "#1769AA",
    "Mars": "#C44536",
    "Jupiter": "#8054A1",
    "Saturn": "#9A6700",
    "Uranus": "#00838F",
    "Neptune": "#3F51B5"
}

FRAGMENT_COLORS = [
    "#0072B2",
    "#D55E00",
    "#009E73",
    "#CC79A7",
    "#E69F00",
    "#56B4E9",
    "#8C564B",
    "#4C78A8",
    "#B279A2",
    "#2F6B4F",
    "#B23A48",
    "#6B5CA5",
    "#7A6A00",
    "#277DA1",
    "#F28E2B",
    "#5B8E7D",
    "#A05195",
    "#3D5A80",
    "#BC6C25",
    "#577590",
]


st.set_page_config(
    page_title="COMETRA",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)


# Comet data used by JPL
comets = {
    "2P/Encke": {
        "id": "90000032;",
        "designation": "2P"
    },
    "1P/Halley": {
        "id": "1P;",
        "designation": "1P"
    },
    "67P/Churyumov-Gerasimenko": {
        "id": "90000703;",
        "designation": "67P"
    },
    "9P/Tempel 1": {
        "id": "9P;",
        "designation": "9P"
    },
    "103P/Hartley 2": {
        "id": "103P;",
        "designation": "103P"
    }
}


st.title("COMETRA")


with st.sidebar:

    st.header("Simulation")

    selectedComet = st.selectbox(
        "Comet",
        list(comets.keys())
    )

    cometData = comets[selectedComet]

    st.divider()

    st.subheader("Fragmentation Event")

    fragmentationDateColumn, fragmentationTimeColumn = st.columns(2)
    with fragmentationDateColumn:
        fragmentationDate = st.date_input(
            "Fragmentation date",
            value=date(2027, 1, 1),
            min_value=date(1900, 1, 1),
            max_value=date(2200, 12, 31)
        )

    with fragmentationTimeColumn:
        fragmentationTime = st.time_input(
            "Fragmentation time",
            value=time(12, 0)
        )

    st.subheader("Simulation End")

    simulationEndDateColumn, simulationEndTimeColumn = st.columns(2)
    with simulationEndDateColumn:
        simulationEndDate = st.date_input(
            "Simulation end date",
            value=date(2030, 1, 1),
            min_value=date(1900, 1, 1),
            max_value=date(2200, 12, 31)
        )

    with simulationEndTimeColumn:
        simulationEndTime = st.time_input(
            "Simulation end time",
            value=time(12, 0)
        )

    st.divider()

    st.subheader("Fragmentation Parameters")

    fragmentCount = st.number_input(
        "Number of fragments",
        min_value=1,
        max_value=20,
        value=3,
        step=1
    )

    st.caption(
        "X, Y, and Z values are velocity components in m/s added to "
        "the comet's JPL velocity at the fragmentation event."
    )

    separationVelocities = []

    for i in range(int(fragmentCount)):

        with st.expander(
            f"Fragment F{i + 1}",
            expanded=(i == 0)
        ):

            xVelocity = st.number_input(
                "X velocity (m/s)",
                value=float((i + 1) * 100),
                step=10.0,
                key=f"fragmentX{i}"
            )

            yVelocity = st.number_input(
                "Y velocity (m/s)",
                value=float((i + 1) * 50),
                step=10.0,
                key=f"fragmentY{i}"
            )

            zVelocity = st.number_input(
                "Z velocity (m/s)",
                value=0.0,
                step=10.0,
                key=f"fragmentZ{i}"
            )

            separationVelocities.append(
                (
                    xVelocity,
                    yVelocity,
                    zVelocity
                )
            )

    st.divider()

    st.subheader("Visualization")

    viewMode = st.radio(
        "View",
        [
            "Full Solar System",
            "Inner Solar System",
            "Fragmentation Area"
        ],
        index=0
    )

    with st.expander("Display options"):
        maxAnimationFrames = st.slider(
            "Animation frames",
            min_value=50,
            max_value=500,
            value=250,
            step=25
        )

        trajectoryPoints = st.slider(
            "Trajectory points",
            min_value=100,
            max_value=2000,
            value=800,
            step=100
        )

    st.divider()

    runSimulation = st.button(
        "Run Simulation"
    )


def sampleIndices(
    totalCount,
    maximumCount
):

    if totalCount <= maximumCount:

        return list(
            range(totalCount)
        )

    return list(
        np.linspace(
            0,
            totalCount - 1,
            maximumCount,
            dtype=int
        )
    )


def getXYPosition(
    position
):

    return (
        position[0] / 1.496e11,
        position[1] / 1.496e11
    )


def getTrajectoryPath(
    body,
    collisions,
    maximumCount
):
    indices = sampleIndices(
        len(body.trajectory),
        maximumCount
    )
    trajectoryPoints = [
        (
            body.trajectoryTimes[index],
            getXYPosition(body.trajectory[index])
        )
        for index in indices
    ]

    for collision in collisions:
        if collision["bodyA"] == body.CelesName:
            position = collision["positionA"]
        elif collision["bodyB"] == body.CelesName:
            position = collision["positionB"]
        else:
            continue

        bracketIndex = bisect_left(
            body.trajectoryTimes,
            collision["time"]
        )
        for index in (bracketIndex - 1, bracketIndex):
            if 0 <= index < len(body.trajectory):
                trajectoryPoints.append(
                    (
                        body.trajectoryTimes[index],
                        getXYPosition(body.trajectory[index])
                    )
                )

        trajectoryPoints.append(
            (
                collision["time"],
                getXYPosition(position)
            )
        )

    trajectoryPoints.sort(
        key=lambda point: point[0]
    )

    return [
        point[1]
        for point in trajectoryPoints
    ]


def createPlot(
    result
):

    solarSystem = result["solarSystem"]
    comet = result["comet"]
    cometBaselinePositions = result["cometBaselinePositions"]
    fragments = result["fragments"]
    fragmentationPoint = result["fragmentationPoint"]
    collisions = result["collisions"]

    planets = []

    for body in solarSystem.bodies:

        if body.CelesName in PLANET_COLORS:

            planets.append(body)

    figure = go.Figure()

    # Sun
    figure.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers",
            name="Sun",
            legendgroup="Sun",
            marker=dict(
                size=12,
                symbol="circle",
                color="#E0A800",
                line=dict(color="#725500", width=1)
            ),
            hovertemplate=(
                "<b>Sun</b>"
                "<extra></extra>"
            )
        )
    )

    # Planet paths
    for planet in planets:
        sampledTrajectory = getTrajectoryPath(
            planet,
            collisions,
            trajectoryPoints
        )

        xValues = [
            position[0]
            for position in sampledTrajectory
        ]

        yValues = [
            position[1]
            for position in sampledTrajectory
        ]

        figure.add_trace(
            go.Scatter(
                x=xValues,
                y=yValues,
                mode="lines",
                name=f"{planet.CelesName} orbit",
                legendgroup=planet.CelesName,
                line=dict(
                    color=PLANET_COLORS[planet.CelesName],
                    dash="solid",
                    width=1.5
                ),
                hoverinfo="skip"
            )
        )

    # Plot the unmodified position vectors copied from the JPL ephemeris.
    cometTrajectory = [
        getXYPosition(position)
        for position in cometBaselinePositions
    ]

    figure.add_trace(
        go.Scatter(
            x=[position[0] for position in cometTrajectory],
            y=[position[1] for position in cometTrajectory],
            mode="lines",
            name=f"{comet.CelesName} JPL baseline",
            legendgroup="comet-baseline",
            line=dict(color="#273746", dash="dash", width=2.5)
        )
    )

    # Fragment paths
    for fragmentIndex, fragment in enumerate(fragments):
        sampledTrajectory = getTrajectoryPath(
            fragment,
            collisions,
            trajectoryPoints
        )

        xValues = [
            position[0]
            for position in sampledTrajectory
        ]

        yValues = [
            position[1]
            for position in sampledTrajectory
        ]

        figure.add_trace(
            go.Scatter(
                x=xValues,
                y=yValues,
                mode="lines",
                name=f"{fragment.FragmentID} trajectory",
                legendgroup=fragment.FragmentID,
                line=dict(
                    color=FRAGMENT_COLORS[
                        fragmentIndex % len(FRAGMENT_COLORS)
                    ],
                    dash="solid",
                    width=2.5
                )
            )
        )

    # These traces are updated during animation
    animatedTraceIndices = []
    bodyMarkerTraceIndices = {}

    sunTraceIndex = len(figure.data)
    bodyMarkerTraceIndices["Sun"] = sunTraceIndex
    sunPoint = 0
    sunPosition = getXYPosition(
        solarSystem.bodies[0].trajectory[sunPoint]
    )

    figure.add_trace(
        go.Scatter(
            x=[sunPosition[0]],
            y=[sunPosition[1]],
            mode="markers",
            name="Sun",
            legendgroup="Sun",
            showlegend=False,
            marker=dict(
                size=12,
                symbol="circle",
                color="#E0A800",
                line=dict(color="#725500", width=1)
            )
        )
    )

    animatedTraceIndices.append(
        sunTraceIndex
    )

    for planet in planets:

        planetTraceIndex = len(figure.data)
        bodyMarkerTraceIndices[planet.CelesName] = planetTraceIndex
        planetPoint = 0
        planetPosition = getXYPosition(
            planet.trajectory[planetPoint]
        )

        figure.add_trace(
            go.Scatter(
                x=[planetPosition[0]],
                y=[planetPosition[1]],
                mode="markers",
                name=planet.CelesName,
                legendgroup=planet.CelesName,
                showlegend=False,
                marker=dict(
                    size=7,
                    symbol="circle",
                    color=PLANET_COLORS[planet.CelesName],
                    line=dict(color="#FFFFFF", width=1)
                ),
                hovertemplate=(
                    f"<b>{planet.CelesName}</b>"
                    "<extra></extra>"
                )
            )
        )

        animatedTraceIndices.append(
            planetTraceIndex
        )

    # Main comet
    cometTraceIndex = len(figure.data)
    bodyMarkerTraceIndices[comet.CelesName] = cometTraceIndex
    cometPoint = 0

    figure.add_trace(
        go.Scatter(
            x=[cometTrajectory[cometPoint][0]],
            y=[cometTrajectory[cometPoint][1]],
            mode="markers",
            name="Main comet",
            legendgroup="comet-baseline",
            showlegend=False,
            marker=dict(
                size=11,
                symbol="diamond",
                color="#273746",
                line=dict(color="#FFFFFF", width=1)
            ),
            hovertemplate=(
                f"<b>{comet.CelesName}</b>"
                "<br>JPL baseline"
                "<extra></extra>"
            )
        )
    )

    animatedTraceIndices.append(
        cometTraceIndex
    )

    # Fragment markers
    for fragmentIndex, fragment in enumerate(fragments):

        fragmentTraceIndex = len(figure.data)
        bodyMarkerTraceIndices[fragment.CelesName] = fragmentTraceIndex
        fragmentColor = FRAGMENT_COLORS[
            fragmentIndex % len(FRAGMENT_COLORS)
        ]

        figure.add_trace(
            go.Scatter(
                x=[],
                y=[],
                mode="markers+text",
                name=f"Fragment {fragment.FragmentID}",
                legendgroup=fragment.FragmentID,
                showlegend=False,
                text=[],
                textposition="top center",
                marker=dict(
                    size=10,
                    symbol="circle",
                    color=fragmentColor,
                    line=dict(color="#FFFFFF", width=1)
                ),
                hovertemplate=(
                    f"<b>{fragment.FragmentID}</b>"
                    "<br>Hypothetical fragment"
                    "<extra></extra>"
                )
            )
        )

        animatedTraceIndices.append(
            fragmentTraceIndex
        )

    # Fragmentation point
    fragmentationPosition = comet.trajectory[
        fragmentationPoint
    ]

    fragmentationX, fragmentationY = getXYPosition(
        fragmentationPosition
    )

    figure.add_trace(
        go.Scatter(
            x=[fragmentationX],
            y=[fragmentationY],
            mode="markers",
            name="Fragmentation point",
            marker=dict(
                size=9,
                symbol="x",
                color="#7B2CBF",
                line=dict(color="#7B2CBF", width=2)
            ),
            hovertemplate=(
                "<b>Fragmentation point</b>"
                "<extra></extra>"
            )
        )
    )

    collisionTraceIndex = len(figure.data)
    figure.add_trace(
        go.Scatter(
            x=[],
            y=[],
            mode="markers+text",
            name="Collision",
            legendgroup="collision",
            showlegend=False,
            text=[],
            textposition="top center",
            marker=dict(
                size=24,
                symbol="circle-open",
                color="#c0392b",
                line=dict(
                    color="#c0392b",
                    width=3
                )
            ),
            visible=False,
            hovertemplate=(
                "<b>Collision</b>"
                "<extra></extra>"
            )
        )
    )

    # Create animation frames
    totalPoints = len(cometBaselinePositions)

    animationIndices = sampleIndices(
        totalPoints,
        maxAnimationFrames
    )
    collisionIndices = [
        getCollisionFrameIndex(
            collision,
            result["cometBaselineTimes"]
        )
        for collision in collisions
    ]
    animationIndices = sorted(
        set(animationIndices + collisionIndices)
    )

    frames = []

    for mainPoint in animationIndices:

        frameData = []

        sun = solarSystem.bodies[0]

        sunPoint = min(
            mainPoint,
            len(sun.trajectory) - 1
        )

        sunPosition = getXYPosition(
            sun.trajectory[sunPoint]
        )

        frameData.append(
            go.Scatter(
                x=[sunPosition[0]],
                y=[sunPosition[1]]
            )
        )

        for planet in planets:

            planetPoint = min(
                mainPoint,
                len(planet.trajectory) - 1
            )

            planetPosition = getXYPosition(
                planet.trajectory[planetPoint]
            )

            frameData.append(
                go.Scatter(
                    x=[planetPosition[0]],
                    y=[planetPosition[1]]
                )
            )

        cometPoint = min(
            mainPoint,
            len(cometBaselinePositions) - 1
        )

        cometPosition = getXYPosition(
            cometBaselinePositions[cometPoint]
        )

        frameData.append(
            go.Scatter(
                x=[cometPosition[0]],
                y=[cometPosition[1]]
            )
        )

        # Hide fragments until the breakup point
        for fragment in fragments:

            if mainPoint < fragmentationPoint:

                frameData.append(
                    go.Scatter(
                        x=[],
                        y=[],
                        text=[]
                    )
                )

                continue

            fragmentPoint = (
                mainPoint
                - fragmentationPoint
            )

            fragmentPoint = min(
                fragmentPoint,
                len(fragment.trajectory) - 1
            )

            fragmentPosition = getXYPosition(
                fragment.trajectory[fragmentPoint]
            )

            frameData.append(
                go.Scatter(
                    x=[fragmentPosition[0]],
                    y=[fragmentPosition[1]],
                    text=[fragment.FragmentID]
                )
            )

        frames.append(
            go.Frame(
                name=str(mainPoint),
                data=frameData,
                traces=animatedTraceIndices
            )
        )

    figure.frames = frames

    if viewMode == "Inner Solar System":

        figure.update_xaxes(
            range=[-5, 5]
        )

        figure.update_yaxes(
            range=[-5, 5]
        )

    elif viewMode == "Fragmentation Area":

        distanceFromSun = max(
            abs(fragmentationX),
            abs(fragmentationY)
        )

        viewSize = max(
            2,
            min(
                20,
                distanceFromSun * 0.25
            )
        )

        figure.update_xaxes(
            range=[
                fragmentationX - viewSize,
                fragmentationX + viewSize
            ]
        )

        figure.update_yaxes(
            range=[
                fragmentationY - viewSize,
                fragmentationY + viewSize
            ]
        )

    figure.update_layout(
        height=780,
        xaxis=dict(
            title="X Distance from Sun (AU)",
            scaleanchor="y",
            scaleratio=1,
            showgrid=True,
            gridcolor="#E5E9EF",
            zerolinecolor="#AAB4C0"
        ),
        yaxis=dict(
            title="Y Distance from Sun (AU)",
            showgrid=True,
            gridcolor="#E5E9EF",
            zerolinecolor="#AAB4C0"
        ),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#263238"),
        legend=dict(
            title="Legend",
            orientation="h",
            x=0,
            y=1.16,
            xanchor="left",
            yanchor="bottom",
            bgcolor="rgba(255,255,255,0.92)",
            bordercolor="#C7D0D9",
            borderwidth=1,
            groupclick="togglegroup",
            font=dict(size=11)
        ),
        hovermode="closest",
        margin=dict(
            l=60,
            r=30,
            t=120,
            b=80
        ),
        meta={
            "collisionTraceIndex": collisionTraceIndex,
            "bodyMarkerTraceIndices": bodyMarkerTraceIndices
        }
    )

    return figure


# Run the simulation
if runSimulation:

    fragmentationDateTime = datetime.combine(
        fragmentationDate,
        fragmentationTime
    )

    simulationEndDateTime = datetime.combine(
        simulationEndDate,
        simulationEndTime
    )

    if simulationEndDateTime <= fragmentationDateTime:

        st.error(
            "Simulation end date and time must be "
            "after the fragmentation event."
        )

        st.stop()

    config = SimulationConfig(
        cometName=selectedComet,
        cometID=cometData["id"],
        cometDesignation=cometData["designation"],
        fragmentationDate=(
            fragmentationDateTime.strftime(
                "%Y-%m-%d %H:%M"
            )
        ),
        simulationEndDate=(
            simulationEndDateTime.strftime(
                "%Y-%m-%d %H:%M"
            )
        ),
        separationVelocities=separationVelocities
    )

    with st.spinner(
        "Loading JPL data and running simulation..."
    ):

        try:

            runner = SimulationRunner()

            result = runner.run(config)

            st.session_state[
                "simulationResult"
            ] = result

            st.session_state[
                "simulationConfig"
            ] = config

        except Exception as error:

            st.error(
                f"Simulation failed: {error}"
            )

            st.stop()


# Display results
if "simulationResult" in st.session_state:

    result = st.session_state["simulationResult"]

    comet = result["comet"]
    fragments = result["fragments"]

    st.header("Simulation Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Selected comet",
            comet.CelesName
        )

    with col2:

        st.metric(
            "Fragments",
            len(fragments)
        )

    with col3:

        st.metric(
            "JPL time step",
            result["jplStep"]
        )

    with col4:

        st.metric(
            "Physics time step",
            f"{result['timeStep']} s"
        )

    st.divider()

    periodCol1, periodCol2, periodCol3 = st.columns(3)

    with periodCol1:

        st.caption("Simulation start")

        st.write(
            result["simulationStartDate"].strftime(
                "%Y-%m-%d %H:%M"
            )
        )

    with periodCol2:

        st.caption("Fragmentation event")

        st.write(
            result["fragmentationDate"].strftime(
                "%Y-%m-%d %H:%M"
            )
        )

    with periodCol3:

        st.caption("Simulation end")

        st.write(
            result["simulationEndDate"].strftime(
                "%Y-%m-%d %H:%M"
            )
        )

    st.divider()

    st.header("Orbital Visualization")

    if not result["collisions"]:
        st.info(
            "No collisions were detected for the simulated period. "
            "Detection uses a 1 km fragment radius and known solar-body radii."
        )

    figure = createPlot(result)
    st.caption(
        "Normal Play runs through the full simulation. Collision Play "
        "starts at the beginning and pauses at each detected collision; "
        "select Continue to resume."
    )
    st.iframe(
        createPlaybackHtml(result, figure),
        height=940
    )

    st.divider()

    st.header("Fragment Analysis")

    fragmentRows = []

    for fragment, separationVelocity in zip(
        fragments,
        result["separationVelocities"]
    ):

        separationSpeed = np.linalg.norm(
            separationVelocity
        )

        fragmentRows.append(
            {
                "Fragment": fragment.FragmentID,
                "X velocity (m/s)": round(
                    separationVelocity[0],
                    2
                ),
                "Y velocity (m/s)": round(
                    separationVelocity[1],
                    2
                ),
                "Z velocity (m/s)": round(
                    separationVelocity[2],
                    2
                ),
                "Separation speed (m/s)": round(
                    separationSpeed,
                    2
                )
            }
        )

    st.dataframe(
        fragmentRows,
        width="stretch",
        hide_index=True
    )

    st.divider()

    st.header("Closest Earth Approaches")

    approachRows = []

    for approach in result["closestApproaches"]:

        distanceKm = (
            approach["distance"] / 1000
        )

        distanceAU = (
            approach["distance"] / 1.496e11
        )

        fragment = approach["fragment"]

        approachRows.append(
            {
                "Fragment": fragment.FragmentID,
                "Minimum distance (km)": round(
                    distanceKm,
                    2
                ),
                "Minimum distance (AU)": round(
                    distanceAU,
                    6
                ),
                "Time": approach["time"].strftime(
                    "%Y-%m-%d %H:%M"
                )
            }
        )

    if len(approachRows) > 0:

        st.dataframe(
            approachRows,
            width="stretch",
            hide_index=True
        )

    else:

        st.info(
            "No Earth approach data is available."
        )

    st.divider()

    with st.expander("Simulation model"):

        st.write(
            "The Sun and planets are represented "
            "using JPL Horizons ephemeris data. "
            "The original comet follows its JPL "
            "baseline trajectory. After the "
            "configured fragmentation event, "
            "individual fragment trajectories "
            "are calculated using gravitational "
            "acceleration and the configured "
            "separation velocities."
        )

        st.write(
            "Collision checks use a 1 km spherical radius for each "
            "fragment and published mean radii for the Sun and planets. "
            "Contacts are interpolated between trajectory samples. "
            "Collision playback pauses at each detected contact, but "
            "impact effects are not modeled; trajectories continue "
            "unchanged after a contact."
        )
else:

    st.header("Ready")

    st.info(
        "Configure the simulation parameters "
        "in the sidebar and select Run Simulation."
    )