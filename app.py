import streamlit as st
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, date, time

from simulation_runner import SimulationRunner
from simulation_config import SimulationConfig


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
        "id": "67P;",
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

    fragmentationDate = st.date_input(
        "Date",
        value=date(2027, 1, 1),
        min_value=date(1900, 1, 1),
        max_value=date(2200, 12, 31)
    )

    fragmentationTime = st.time_input(
        "Time",
        value=time(12, 0)
    )

    st.subheader("Simulation End")

    simulationEndDate = st.date_input(
        "End Date",
        value=date(2030, 1, 1),
        min_value=date(1900, 1, 1),
        max_value=date(2200, 12, 31)
    )

    simulationEndTime = st.time_input(
        "End Time",
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
        "Separation velocity relative to the "
        "original comet at fragmentation."
    )

    separationVelocities = []

    for i in range(int(fragmentCount)):

        with st.expander(
            f"Fragment F{i + 1}",
            expanded=(i < 3)
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


def createPlot(
    result
):

    solarSystem = result["solarSystem"]
    comet = result["comet"]
    fragments = result["fragments"]
    fragmentationPoint = result["fragmentationPoint"]

    planets = []

    for body in solarSystem.bodies:

        if body.CelesName in [
            "Mercury",
            "Venus",
            "Earth",
            "Mars",
            "Jupiter",
            "Saturn",
            "Uranus",
            "Neptune"
        ]:

            planets.append(body)

    figure = go.Figure()

    # Sun
    figure.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers",
            name="Sun",
            marker=dict(
                size=12,
                symbol="circle"
            ),
            hovertemplate=(
                "<b>Sun</b>"
                "<extra></extra>"
            )
        )
    )

    # Planet paths
    for planet in planets:

        trajectory = [
            getXYPosition(position)
            for position in planet.trajectory
        ]

        indices = sampleIndices(
            len(trajectory),
            trajectoryPoints
        )

        xValues = [
            trajectory[i][0]
            for i in indices
        ]

        yValues = [
            trajectory[i][1]
            for i in indices
        ]

        figure.add_trace(
            go.Scatter(
                x=xValues,
                y=yValues,
                mode="lines",
                name=f"{planet.CelesName} orbit",
                line=dict(
                    dash="dot",
                    width=1
                ),
                hoverinfo="skip",
                showlegend=False
            )
        )

    # Original comet path from JPL
    cometTrajectory = [
        getXYPosition(position)
        for position in comet.trajectory
    ]

    cometIndices = sampleIndices(
        len(cometTrajectory),
        trajectoryPoints
    )

    cometX = [
        cometTrajectory[i][0]
        for i in cometIndices
    ]

    cometY = [
        cometTrajectory[i][1]
        for i in cometIndices
    ]

    figure.add_trace(
        go.Scatter(
            x=cometX,
            y=cometY,
            mode="lines",
            name=f"{comet.CelesName} JPL baseline",
            line=dict(
                dash="dot",
                width=2
            )
        )
    )

    # Fragment paths
    for fragment in fragments:

        trajectory = [
            getXYPosition(position)
            for position in fragment.trajectory
        ]

        indices = sampleIndices(
            len(trajectory),
            trajectoryPoints
        )

        xValues = [
            trajectory[i][0]
            for i in indices
        ]

        yValues = [
            trajectory[i][1]
            for i in indices
        ]

        figure.add_trace(
            go.Scatter(
                x=xValues,
                y=yValues,
                mode="lines",
                name=f"{fragment.FragmentID} trajectory",
                line=dict(
                    dash="dot",
                    width=2
                )
            )
        )

    # These traces are updated during animation
    animatedTraceIndices = []

    sunTraceIndex = len(figure.data)

    figure.add_trace(
        go.Scatter(
            x=[0],
            y=[0],
            mode="markers",
            name="Sun position",
            marker=dict(
                size=12,
                symbol="circle"
            )
        )
    )

    animatedTraceIndices.append(
        sunTraceIndex
    )

    for planet in planets:

        planetTraceIndex = len(figure.data)

        figure.add_trace(
            go.Scatter(
                x=[0],
                y=[0],
                mode="markers",
                name=planet.CelesName,
                marker=dict(
                    size=7,
                    symbol="circle"
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

    figure.add_trace(
        go.Scatter(
            x=[cometX[0]],
            y=[cometY[0]],
            mode="markers",
            name="Main comet",
            marker=dict(
                size=11,
                symbol="circle"
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
    for fragment in fragments:

        fragmentTraceIndex = len(figure.data)

        figure.add_trace(
            go.Scatter(
                x=[],
                y=[],
                mode="markers+text",
                name=f"Fragment {fragment.FragmentID}",
                text=[],
                textposition="top center",
                marker=dict(
                    size=10,
                    symbol="circle"
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
                symbol="x"
            ),
            hovertemplate=(
                "<b>Fragmentation point</b>"
                "<extra></extra>"
            )
        )
    )

    # Create animation frames
    totalPoints = len(comet.trajectory)

    animationIndices = sampleIndices(
        totalPoints,
        maxAnimationFrames
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
            len(comet.trajectory) - 1
        )

        cometPosition = getXYPosition(
            comet.trajectory[cometPoint]
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
                + 1
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
            scaleratio=1
        ),
        yaxis=dict(
            title="Y Distance from Sun (AU)"
        ),
        hovermode="closest",
        margin=dict(
            l=60,
            r=30,
            t=120,
            b=80
        ),
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                x=0.02,
                y=1.08,
                xanchor="left",
                yanchor="bottom",
                buttons=[
                    dict(
                        label="Play",
                        method="animate",
                        args=[
                            None,
                            {
                                "frame": {
                                    "duration": 80,
                                    "redraw": True
                                },
                                "transition": {
                                    "duration": 0
                                },
                                "fromcurrent": True
                            }
                        ]
                    ),
                    dict(
                        label="Pause",
                        method="animate",
                        args=[
                            [None],
                            {
                                "frame": {
                                    "duration": 0,
                                    "redraw": False
                                },
                                "mode": "immediate"
                            }
                        ]
                    )
                ]
            )
        ],
        sliders=[
            dict(
                active=0,
                x=0.22,
                y=1.08,
                len=0.73,
                currentvalue=dict(
                    prefix="Simulation point: "
                ),
                steps=[
                    dict(
                        label=str(index),
                        method="animate",
                        args=[
                            [str(index)],
                            {
                                "frame": {
                                    "duration": 0,
                                    "redraw": True
                                },
                                "mode": "immediate"
                            }
                        ]
                    )
                    for index in animationIndices
                ]
            )
        ]
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

    figure = createPlot(result)

    st.plotly_chart(
        figure,
        use_container_width=True,
        config={
            "scrollZoom": True,
            "displaylogo": False,
            "responsive": True
        }
    )

    st.divider()

    st.header("Fragment Analysis")

    fragmentRows = []

    for fragment in fragments:

        separationVelocity = (
            fragment.CelesVelocity
            - comet.CelesVelocity
        )

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
        use_container_width=True,
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
            use_container_width=True,
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

else:

    st.header("Ready")

    st.info(
        "Configure the simulation parameters "
        "in the sidebar and select Run Simulation."
    )