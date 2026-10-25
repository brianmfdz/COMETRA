# COMETRA

COMETRA is a comet fragmentation simulator I developed using Python, Streamlit, and Plotly. I can select a comet, choose when it breaks apart, and set the velocity of each fragment.

The simulator tracks how the fragments move through the Solar System under the gravity of the Sun and all eight planets. It also checks for collisions with planets, the Sun, and other fragments.

I use NASA JPL Horizons to obtain real astronomical positions and velocities.


---

## What My Project Can Do

1. Download real astronomical data from NASA JPL Horizons.
2. Split a selected comet into multiple fragments.
3. Set the separation velocity of each fragment using X, Y, and Z values.
4. Calculate fragment movement using gravity from the Sun and all eight planets.
5. Detect collisions and calculate the closest approach to Earth.
6. Display the results using an animated Plotly graph.

---

## Gravity Calculation

- I calculate the gravitational acceleration caused by the Sun and all eight planets on each fragment.
- I combine the gravitational effects of all nine bodies to calculate the total acceleration.
- I use the **leapfrog integration method** to update the fragments' positions and velocities.
- The Sun, planets, and original comet follow the positions and velocities obtained from NASA JPL Horizons.

The simulation time step depends on the simulation length.

| Simulation length | Time step |
|---|---|
| 30 days or less | 1 hour |
| Up to 365 days | 6 hours |
| More than 365 days | 1 day |


---

## Collision Detection

- I treat each fragment as a sphere with a radius of 1 km.
- The Sun and planets use their mean radii.
- I check the path between consecutive time steps to detect possible collisions.
- I also check for collisions between fragments.
- When a collision occurs, I record it and display it in the visualization. I do not simulate the physical effects of the impact.

---

## Visualization

I use Plotly to display and animate the simulation.

- **Normal Play:** Plays the full simulation.
- **Collision Play:** Pauses when a collision occurs.
- **Collision Zoom:** Zooms in on the collision area and displays a red circle around the contact point.
- **Time Slider:** Lets me move to a specific time in the simulation.
- **View Modes:** Full Solar System, Inner Solar System, and Fragmentation Area.


---

## How to Run My Project

I need Python and an internet connection to download the astronomical data.

First, I install the required packages:

```bash
pip install -r requirements.txt
```

Then I start the Streamlit application:

```bash
streamlit run app.py
```

After opening the application, I can select a comet, set the fragmentation and end dates, choose the number of fragments, enter their velocities, and click **Run Simulation**.

---

## How to Test the Simulation

Follow these steps to run the test with two fragments.

### 1. Start the Application

Run the following command in the terminal:

```bash
streamlit run app.py
```

### 2. Simulation Settings

Set the following values in the sidebar.

| Setting | Value |
|---|---|
| Comet | 67P/Churyumov–Gerasimenko |
| Fragmentation date | 2026-01-01 |
| Fragmentation time | 12:00 |
| Simulation end date | 2034-11-24 |
| Simulation end time | 12:00 |
| Number of fragments | 2 |

### 3. Fragmentation Parameters

Open the settings for each fragment and enter the values below.

**Fragment F1**

| Parameter | Velocity (m/s) |
|---|---:|
| X | -285.40 |
| Y | 2751.33 |
| Z | -1383.22 |

**Fragment F2**

| Parameter | Velocity (m/s) |
|---|---:|
| X | 1000 |
| Y | 5000 |
| Z | 1000 |


### 4. Run the Simulation

1. Check that the selected comet, dates, and number of fragments are correct.
2. Verify the velocity components for F1 and F2.
3. Click **Run Simulation**.
4. Once the results appear, click **Collision Play** above the plot.
5. Watch the animation. The simulation pauses when a collision is detected, allowing me to inspect the event.

---

## Project Files

I separated my project into multiple Python files so that each part has its own responsibility. This makes the code easier to understand, maintain, and improve.

| File | Purpose |
|---|---|
| `app.py` | Main interface, inputs, graphs, and tables |
| `playback_view.py` | Animation controls and collision zoom |
| `simulation_runner.py` | Runs the simulation |
| `data_loader.py` | Downloads and reads JPL data |
| `fragment_simulator.py` | Calculates fragment movement |
| `physics_model.py` | Calculates gravity |
| `fragmentation_model.py` | Creates fragments |
| `fragmentation_event.py` | Stores breakup time and fragment velocities |
| `real_body_simulator.py` | Updates celestial body positions using JPL data |
| `jpl_ephemeris.py` | Stores downloaded astronomical data |
| `collision_analysis.py` | Detects collisions |
| `trajectory_analysis.py` | Calculates closest approaches to Earth |
| `celestial_body.py` | Defines classes for planets, comets, and fragments |
| `solar_system.py` | Manages celestial bodies |
| `simulation_config.py` | Stores simulation settings |
| `main.py` | Runs the text-based simulator |
| `simulator.py` | Older simulator not used by the main application |

---

## Limitations

- I do not include the gravitational influence of fragments on each other or on the planets.
- The Moon is not included in the simulation.
- I only consider gravity. Effects such as comet gas jets and solar radiation pressure are not included.
- Fragment velocities are selected by the user rather than predicted by a breakup model.
- Collision accuracy depends partly on the simulation time step.
- Impact effects are not simulated.

---

## Basic Viva Questions

**1. Where do I get the astronomical data?**

I use NASA JPL Horizons to obtain astronomical positions and velocities.

**2. How do I calculate gravity?**

I calculate and combine the gravitational acceleration from the Sun and all eight planets for each fragment.

**3. Why do I use the leapfrog method?**

I use it to update fragment positions and velocities during the simulation. It is suitable for orbital calculations because of its good long-term energy behaviour.

**4. How do I detect collisions?**

I check whether the path between consecutive time steps comes within the combined collision radius of a fragment and another body.

**5. What technologies do I use?**

I use Python for the simulation, Streamlit for the interface, Plotly for visualization, and NASA JPL Horizons for astronomical data.
