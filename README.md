# Fire Evacuation Boids Model

A Python simulation using the Boids algorithm to model crowd evacuation behavior through multiple rooms. The simulation uses pygame for visualization and implements a sequential exit system with configurable flow rates.


## Requirements

```bash
python >= 3.8
pygame >= 2.0.0
opencv-python >= 4.0.0
numpy >= 1.19.0
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Fire-Evacuation-Boids-Model.git
cd Fire-Evacuation-Boids-Model
```

2. Install required dependencies:
```bash
pip install pygame opencv-python numpy
```

## Usage

Run the simulation:
```bash
python main.py
```

### Controls
- `ESC`: Exit simulation
- `R`: Toggle video recording

## Configuration

All simulation parameters can be adjusted in `config.py`:

### Room Layout
```python
ROOMS = {
    1: {
        "bounds": (x, y, width, height),
        "spawn_area": (x, y, width, height),
        "exits": [
            {
                "id": 1,
                "to_room": 2,
                "position": (x, y),
                "flow_rate": boids_per_second,
                "width": pixels
            },
            # ... additional exits
        ]
    },
    # ... additional rooms
}
```

### Boid Parameters
```python
NUM_BOIDS = 10
BOID_RADIUS = 5
ALIGNMENT_STRENGTH = 0.05
COHESION_STRENGTH = 0.01
SEPARATION_STRENGTH = 0.05
WALL_AVOIDANCE_STRENGTH = 0.1
EXIT_STRENGTH = 0.3
MAX_SPEED = 3
```

### Exit Flow Control
```python
EXIT_QUEUE_MAX_SIZE = 5
EXIT_PROCESSING_TIME = {
    1: 1000,  # milliseconds per boid
    2: 333,   # for 3 boids per second
    # ... additional exit timings
}
```

## Project Structure

- `main.py`: Entry point of the simulation
- `simulation.py`: Main simulation logic
- `boid.py`: Boid class implementation
- `map_utils.py`: Map and wall management
- `exit_manager.py`: Exit and queue management
- `config.py`: Configuration parameters

## How It Works

1. **Room System**: Each room is defined with specific boundaries and exit points.

2. **Boid Behavior**: Boids follow three main rules:
   - Alignment: Match velocity with nearby boids
   - Cohesion: Move toward center of nearby boids
   - Separation: Avoid getting too close to others

3. **Exit System**: 
   - Each exit has a maximum queue capacity
   - Boids must wait their turn based on flow rate
   - Controlled transition between rooms




