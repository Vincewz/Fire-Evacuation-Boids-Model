import pygame

# Window configuration
WIDTH, HEIGHT = 1600, 1000  # Augmenté pour une plus grande carte
BACKGROUND_COLOR = (30, 30, 30)
WALL_COLOR = (100, 100, 100)
EXIT_COLOR = (0, 255, 100)
DOOR_COLOR = (200, 200, 0)

# Boid parameters
NUM_BOIDS = 50  
BOID_RADIUS = 5
BOID_COLOR = (100, 200, 255)
ALIGNMENT_STRENGTH = 0.05
COHESION_STRENGTH = 0.01
SEPARATION_STRENGTH = 0.05
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
    1: {  # Starting room (grande salle centrale)
        "bounds": (400, 300, 400, 400),
        "spawn_area": (420, 320, 360, 360),
        "exits": [
            {
                "id": 1,
                "to_room": 2,
                "position": (800, 400),
                "spawn_point": (820, 400),
                "direction": (1, 0),
                "flow_rate": 2,
                "width": 40
            },
            {
                "id": 2,
                "to_room": 3,
                "position": (400, 700),
                "spawn_point": (400, 720),
                "direction": (0, 1),
                "flow_rate": 2,
                "width": 40
            },
            {
                "id": 3,
                "to_room": 4,
                "position": (400, 300),
                "spawn_point": (400, 280),
                "direction": (0, -1),
                "flow_rate": 2,
                "width": 40
            }
        ]
    },
    2: {  # Salle droite
        "bounds": (800, 300, 300, 400),
        "spawn_area": (820, 320, 260, 360),
        "exits": [
            {
                "id": 4,
                "to_room": 5,
                "position": (1100, 500),
                "spawn_point": (1120, 500),
                "direction": (1, 0),
                "flow_rate": 3,
                "width": 40
            },
            {
                "id": 5,
                "to_room": 6,
                "position": (950, 700),
                "spawn_point": (950, 720),
                "direction": (0, 1),
                "flow_rate": 2,
                "width": 40
            }
        ]
    },
    3: {  # Salle bas
        "bounds": (300, 700, 600, 200),
        "spawn_area": (320, 720, 560, 160),
        "exits": [
            {
                "id": 6,
                "to_room": 6,
                "position": (900, 800),
                "spawn_point": (920, 800),
                "direction": (1, 0),
                "flow_rate": 3,
                "width": 40
            },
            {
                "id": 7,
                "to_room": None,
                "position": (300, 800),
                "spawn_point": None,
                "direction": (-1, 0),
                "flow_rate": 3,
                "width": 40
            }
        ]
    },
    4: {  # Salle haut
        "bounds": (300, 100, 600, 200),
        "spawn_area": (320, 120, 560, 160),
        "exits": [
            {
                "id": 8,
                "to_room": 5,
                "position": (900, 200),
                "spawn_point": (920, 200),
                "direction": (1, 0),
                "flow_rate": 2,
                "width": 40
            },
            {
                "id": 9,
                "to_room": None,
                "position": (300, 200),
                "spawn_point": None,
                "direction": (-1, 0),
                "flow_rate": 3,
                "width": 40
            }
        ]
    },
    5: {  # Salle haut droite
        "bounds": (1100, 100, 200, 400),
        "spawn_area": (1120, 120, 160, 360),
        "exits": [
            {
                "id": 10,
                "to_room": None,
                "position": (1300, 300),
                "spawn_point": None,
                "direction": (1, 0),
                "flow_rate": 3,
                "width": 40
            }
        ]
    },
    6: {  # Salle bas droite
        "bounds": (900, 700, 400, 200),
        "spawn_area": (920, 720, 360, 160),
        "exits": [
            {
                "id": 11,
                "to_room": None,
                "position": (1300, 800),
                "spawn_point": None,
                "direction": (1, 0),
                "flow_rate": 3,
                "width": 40
            }
        ]
    }
}

# Exit queues configuration
EXIT_QUEUE_MAX_SIZE = 5
EXIT_PROCESSING_TIME = {
    1: 500,   # 2 boids par seconde
    2: 500,
    3: 500,
    4: 333,   # 3 boids par seconde
    5: 500,
    6: 333,
    7: 333,
    8: 500,
    9: 333,
    10: 333,
    11: 333
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