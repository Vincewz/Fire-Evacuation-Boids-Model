import pygame

# Window configuration
WIDTH, HEIGHT = 1200, 800
BACKGROUND_COLOR = (30, 30, 30)
WALL_COLOR = (100, 100, 100)
EXIT_COLOR = (0, 255, 100)
DOOR_COLOR = (200, 200, 0)

# Boid parameters
NUM_BOIDS = 25
BOID_RADIUS = 5
BOID_COLOR = (100, 200, 255)
ALIGNMENT_STRENGTH = 0.05
COHESION_STRENGTH = 0.01
SEPARATION_STRENGTH = 0.1
WALL_AVOIDANCE_STRENGTH = 0.1
EXIT_STRENGTH = 0.3
MAX_SPEED = 3
VISION_RADIUS = 150
WALL_DETECTION_DISTANCE = 30
EXIT_PASS_DISTANCE = 10

# Wall thickness
WALL_THICKNESS = 10

# Room definitions
ROOMS = {
    1: {
        "bounds": (100, 100, 400, 300),  # x, y, width, height
        "spawn_area": (120, 120, 360, 260),  # Area where boids can spawn
        "exits": [
            {
                "id": 1,
                "to_room": 2,
                "position": (500, 150),
                "spawn_point": (520, 150),  # Where boids appear in next room
                "direction": (1, 0),  # Direction of the exit
                "flow_rate": 1,  # Boids per second
                "width": 30  # Exit width
            },
            {
                "id": 2,
                "to_room": 3,
                "position": (400, 400),
                "spawn_point": (400, 420),
                "direction": (0, 1),
                "flow_rate": 2,
                "width": 40
            }
        ]
    },
    2: {
        "bounds": (500, 100, 300, 300),
        "spawn_area": (520, 120, 260, 260),
        "exits": [
            {
                "id": 3,
                "to_room": 3,
                "position": (600, 400),
                "spawn_point": (600, 420),
                "direction": (0, 1),
                "flow_rate": 3,
                "width": 50
            }
        ]
    },
    3: {
        "bounds": (100, 400, 800, 200),
        "spawn_area": (120, 420, 760, 160),
        "exits": [
            {
                "id": 4,
                "to_room": None,  # None indicates final exit
                "position": (100, 500),
                "spawn_point": None,
                "direction": (-1, 0),
                "flow_rate": 2,
                "width": 40
            }
        ]
    }
}

# Exit queues configuration
EXIT_QUEUE_MAX_SIZE = 5  # Maximum number of boids that can wait at an exit
EXIT_PROCESSING_TIME = {  # Time in milliseconds for a boid to pass through exit
    1: 1000,  # 1 second per boid
    2: 333,   # 3 boids per second
    3: 500,   # 2 boids per second
    4: 333    # 3 boids per second
}

# Generate walls based on room definitions
WALLS = []
for room_id, room in ROOMS.items():
    x, y, w, h = room["bounds"]
    # Main room walls
    WALLS.extend([
        pygame.Rect(x, y, w, WALL_THICKNESS),  # Top
        pygame.Rect(x, y + h, w, WALL_THICKNESS),  # Bottom
        pygame.Rect(x, y, WALL_THICKNESS, h),  # Left
        pygame.Rect(x + w, y, WALL_THICKNESS, h)  # Right
    ])