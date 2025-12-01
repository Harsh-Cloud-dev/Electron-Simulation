# Electron Coulomb Interaction Simulation

A real-time 2D physics simulation of charged electrons repelling each other via **Coulomb's law**, built with **Pygame** for visualization and **SimPy** for discrete-event simulation timing.

Electrons move in a bounded rectangular box, interacting through realistic electrostatic forces with proper numerical integration and collision reflection at boundaries.

![Simulation Preview]


<img src="/Users/harsh/files/github/Electron-Simulation/Screenshot 2025-12-01 at 10.48.54 PM.png">  

## Features

- Physically accurate pairwise Coulomb repulsion between electrons
- Numerical integration using explicit Euler method
- Realistic physical constants (electron mass, charge, Coulomb's constant)
- Boundary reflection with velocity reversal
- Smooth real-time visualization using Pygame
- Precise time stepping with SimPy's discrete-event simulation
- Configurable parameters at the top of the script

## Physics Model

- Force between electrons:  
  $ F = k_e \frac{|q_1 q_2|}{r^2} $ (where $ q_1 = q_2 = -e $)
- Acceleration: $ \vec{a} = \vec{F}/m_e $
- Velocity update: $ \vec{v} \gets \vec{v} + \vec{a} \cdot \Delta t $
- Position update: $ \vec{x} \gets \vec{x} + \vec{v} \cdot \Delta t $
- Singularity avoidance for very close approaches
- Elastic reflection at domain boundaries

## Requirements

- Python 3.7+
- Pygame
- SimPy

Install dependencies with:

```bash
pip install pygame simpy
```

## How to Run

```bash
python electron_simulation.py
```

Or if the file is named differently (e.g., `main.py`):

```bash
python main.py
```

Close the window or press the close button to exit.

## Configuration

All key parameters are defined at the top of the file and can be easily be adjusted:

| Parameter             | Description                              | Default Value      |
|-----------------------|------------------------------------------|--------------------|
| `NUM_ELECTRONS`       | Number of electrons                      | 10                 |
| `WIDTH`, `HEIGHT`     | Window size in pixels                    | 1000×800           |
| `SCALE`            | Meters per pixel (spatial scaling)       | 0.1 mm/px (1e-4)   |
| `TIME_STEP`           | Simulation time step                     | 0.5 μs (5e-7 s)    |
| `V0`                  | Initial speed magnitude (max)            | 1000 m/s           |
| `FPS`                 | Rendering framerate                      | 30                 |
| `RADIUS_PIXELS`       | Visual size of electrons                 | 10 px              |

## Example Use Cases

- Educational demo of electrostatic repulsion
- Studying many-body dynamics in 2D plasma-like systems
- Prototyping N-body algorithms
- Visualizing chaotic motion in conservative force fields

## Limitations & Possible Improvements

- O(N²) force calculation – becomes slow for >100 particles
- No soft-core regularization (can have extreme accelerations on close approach)
- Simple Euler integration (Euler) – consider Verlet or RK4 for better stability
- No energy conservation monitoring
- Fixed time step (adaptive stepping could improve accuracy/efficiency)

## License

MIT License – feel free to use, modify, and share.

---

**Author**: Your Name  
**Created**: December 2025

Enjoy watching the chaotic dance of repelling electrons!
```