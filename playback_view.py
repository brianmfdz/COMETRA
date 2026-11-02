from bisect import bisect_left
import json

import streamlit as st
from plotly.offline import get_plotlyjs


def getCollisionFrameIndex(collision, baselineTimes):
    frameIndex = bisect_left(
        baselineTimes,
        collision["time"]
    )
    return max(
        0,
        min(len(baselineTimes) - 1, frameIndex)
    )


@st.cache_resource
def getPlotlyLibrary():
    return get_plotlyjs()


def createPlaybackHtml(result, figure):
    frameIndices = [
        int(frame.name)
        for frame in figure.frames
    ]
    frameDates = [
        result["cometBaselineTimes"][index].strftime(
            "%Y-%m-%d %H:%M"
        )
        for index in frameIndices
    ]
    collisions = []
    for collision in result["collisions"]:
        frameIndex = getCollisionFrameIndex(
            collision,
            result["cometBaselineTimes"]
        )
        collisionX, collisionY = getXYPosition(
            collision["position"]
        )
        collisions.append(
            {
                "frameIndex": frameIndex,
                "bodyA": collision["bodyA"],
                "bodyB": collision["bodyB"],
                "time": collision["time"].strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "x": collisionX,
                "y": collisionY,
                "positionA": getXYPosition(
                    collision["positionA"]
                ),
                "positionB": getXYPosition(
                    collision["positionB"]
                ),
                "collisionRadius": collision["collisionRadius"]
            }
        )

    figureJson = figure.to_json().replace(
        "<",
        "\\u003c"
    )
    playbackData = json.dumps(
        {
            "frameIndices": frameIndices,
            "frameDates": frameDates,
            "collisions": collisions,
            "collisionTraceIndex": figure.layout.meta[
                "collisionTraceIndex"
            ],
            "bodyMarkerTraceIndices": figure.layout.meta[
                "bodyMarkerTraceIndices"
            ]
        }
    ).replace(
        "<",
        "\\u003c"
    )

    return f"""
<html>
<head>
<meta charset="utf-8">
<style>
    body {{ margin: 0; background: #fff; color: #17212b; font-family: Arial, sans-serif; }}
    .controls {{ display: flex; align-items: center; gap: 8px; padding: 10px 12px; border: 1px solid #c7d0d9; background: #f4f6f8; }}
    button {{ border: 1px solid #7b8794; border-radius: 3px; padding: 8px 14px; background: #fff; color: #17212b; font-size: 14px; cursor: pointer; }}
    button:hover:enabled {{ background: #e7edf2; }}
    button:disabled {{ color: #718096; cursor: default; }}
    #continue {{ border-color: #7b8794; font-weight: 600; }}
    #time {{ min-width: 145px; font-variant-numeric: tabular-nums; font-weight: 600; }}
    #status {{ margin-left: auto; color: #435365; font-size: 13px; }}
    .timeline {{ display: flex; align-items: center; gap: 10px; padding: 4px 12px 0; }}
    input[type=range] {{ width: 100%; }}
    #collision {{ display: none; margin: 4px 12px; border: 1px solid #b42323; border-left: 3px solid #b42323; padding: 6px 9px; background: #fff; color: #641c1c; font-size: 13px; }}
    #plot {{ width: 100%; height: 780px; }}
</style>
</head>
<body>
<div class="controls">
    <button id="normal" title="Play the full simulation without stopping at collisions">Normal Play</button>
    <button id="collisionPlay" title="Play from the beginning and pause at each collision" {"disabled" if not collisions else ""}>Collision Play</button>
    <button id="pause" disabled>Pause</button>
    <button id="continue" hidden>Continue</button>
    <span id="time"></span>
    <span id="status">Ready</span>
</div>
<div class="timeline">
    <span>Start</span>
    <input id="timeline" type="range" min="0" max="{max(0, len(frameIndices) - 1)}" value="0">
    <span>End</span>
</div>
<div id="collision" role="status"></div>
<div id="plot"></div>
<script>{getPlotlyLibrary()}</script>
<script>
const data = {playbackData};
const figure = JSON.parse({json.dumps(figureJson)});
const chart = document.getElementById("plot");
const timeline = document.getElementById("timeline");
const timeLabel = document.getElementById("time");
const statusLabel = document.getElementById("status");
const collisionBox = document.getElementById("collision");
const continueButton = document.getElementById("continue");
const pauseButton = document.getElementById("pause");
let cursor = 0;
let isPlaying = false;
let runToken = 0;
let handledCollisions = new Set();
let activeCollision = null;
const originalRanges = {{
    x: figure.layout.xaxis.range,
    y: figure.layout.yaxis.range
}};

function clearCollisionDisplay() {{
    activeCollision = null;
    collisionBox.style.display = "none";
    continueButton.hidden = true;
    Plotly.restyle(chart, {{x: [[]], y: [[]], text: [[]], visible: [false]}}, [data.collisionTraceIndex]);
}}

async function showCollision(collision, collisionIndex) {{
    activeCollision = collision;
    const point = Math.max(0, Math.min(data.frameIndices.length - 1,
        data.frameIndices.indexOf(collision.frameIndex)));
    collisionBox.textContent = "Collision " + (collisionIndex + 1) + " of " +
        data.collisions.length + " | " + collision.bodyA + " with " +
        collision.bodyB + " at " + collision.time;
    collisionBox.style.display = "block";
    continueButton.hidden = false;
    await Plotly.restyle(chart, {{
        x: [[collision.x]],
        y: [[collision.y]],
        text: [["COLLISION"]],
        visible: [true]
    }}, [data.collisionTraceIndex]);
    const positionA = collision.positionA;
    const positionB = collision.positionB;
    const bodyPositions = [
        [collision.bodyA, positionA],
        [collision.bodyB, positionB]
    ];
    for (const [bodyName, position] of bodyPositions) {{
        const traceIndex = data.bodyMarkerTraceIndices[bodyName];
        if (traceIndex !== undefined) {{
            await Plotly.restyle(chart, {{
                x: [[position[0]]],
                y: [[position[1]]]
            }}, [traceIndex]);
        }}
    }}
    const rangeSize = Math.max(
        2 * collision.collisionRadius / 149600000000,
        0.0001
    );
    await Plotly.relayout(chart, {{
        "xaxis.range": [collision.x - rangeSize, collision.x + rangeSize],
        "yaxis.range": [collision.y - rangeSize, collision.y + rangeSize]
    }});
    statusLabel.textContent = "Paused at collision";
    timeLabel.textContent = data.frameDates[point] || collision.time;
}}

function restoreView() {{
    const view = {{}};
    view["xaxis." + (Array.isArray(originalRanges.x) ? "range" : "autorange")] =
        Array.isArray(originalRanges.x) ? originalRanges.x : true;
    view["yaxis." + (Array.isArray(originalRanges.y) ? "range" : "autorange")] =
        Array.isArray(originalRanges.y) ? originalRanges.y : true;
    return Plotly.relayout(chart, view);
}}

async function play(mode, restart) {{
    runToken += 1;
    const thisRun = runToken;
    isPlaying = true;
    if (restart || cursor >= data.frameIndices.length) {{
        cursor = 0;
        handledCollisions = new Set();
        clearCollisionDisplay();
    }} else if (activeCollision) {{
        clearCollisionDisplay();
    }}
    timeline.value = String(cursor);
    statusLabel.textContent = mode === "collision" ? "Collision playback" : "Playing";
    pauseButton.disabled = false;
    continueButton.hidden = true;

    while (isPlaying && thisRun === runToken && cursor < data.frameIndices.length) {{
        const point = data.frameIndices[cursor];
        await Plotly.animate(chart, [String(point)], {{
            mode: "immediate",
            frame: {{duration: 45, redraw: true}},
            transition: {{duration: 0}}
        }});
        if (thisRun !== runToken) return;

        timeLabel.textContent = data.frameDates[cursor];
        timeline.value = String(cursor);
        cursor += 1;

        if (mode === "collision") {{
            const collisionIndex = data.collisions.findIndex((collision, index) =>
                !handledCollisions.has(index) && collision.frameIndex <= point
            );
            if (collisionIndex !== -1) {{
                handledCollisions.add(collisionIndex);
                isPlaying = false;
                pauseButton.disabled = true;
                await showCollision(data.collisions[collisionIndex], collisionIndex);
                return;
            }}
        }}
    }}

    if (thisRun === runToken) {{
        isPlaying = false;
        pauseButton.disabled = true;
        statusLabel.textContent = mode === "collision"
            ? "Collision playback complete"
            : "Playback complete";
    }}
}}

document.getElementById("normal").addEventListener("click", () => play("normal", false));
document.getElementById("collisionPlay").addEventListener("click", () => play("collision", true));
pauseButton.addEventListener("click", () => {{
    isPlaying = false;
    runToken += 1;
    pauseButton.disabled = true;
    statusLabel.textContent = "Paused";
}});
continueButton.addEventListener("click", () => {{
    restoreView().then(() => play("collision", false));
}});
timeline.addEventListener("input", async () => {{
    isPlaying = false;
    runToken += 1;
    clearCollisionDisplay();
    cursor = Number(timeline.value);
    const point = data.frameIndices[cursor];
    await Plotly.animate(chart, [String(point)], {{
        mode: "immediate",
        frame: {{duration: 0, redraw: true}},
        transition: {{duration: 0}}
    }});
    timeLabel.textContent = data.frameDates[cursor];
    statusLabel.textContent = "Ready";
}});

Plotly.newPlot(chart, figure.data, figure.layout, {{
    responsive: true,
    scrollZoom: true,
    displaylogo: false
}}).then(() => Plotly.addFrames(chart, figure.frames));
</script>
</body>
</html>
"""


def getXYPosition(position):
    return (
        position[0] / 1.496e11,
        position[1] / 1.496e11
    )
