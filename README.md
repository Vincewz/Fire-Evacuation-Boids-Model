# Fire-Evacuation-Boids-Model

## Features

- Boid flocking simulation with classic Reynolds rules:
  - Alignment: Boids align their direction with nearby flockmates
  - Cohesion: Boids move toward the center of nearby flockmates
  - Separation: Boids avoid colliding with each other
- Additional behaviors:
  - Wall avoidance: Boids detect and avoid walls
  - Sequential exit targeting: Boids must pass through exit points in a specific order
  - Debug visualization showing completed exit points for each boid

## Requirements

- Python 3.x
- Pygame

## Installation

1. Clone this repository
2. Install the required dependency:
```bash
pip install pygame
```

## Usage

Run the simulation with:
```bash
python main.py
```

```bash
python main.py --record
```

## Project Structure

- `main.py`: Entry point of the simulation
- `simulation.py`: Main simulation loop and visualization
- `boid.py`: Boid class with flocking behavior implementation
- `map_utils.py`: Environment management and collision detection
- `config.py`: Configuration constants and parameters



