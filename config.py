import pygame

SMOKE_AVOIDANCE_RADIUS = 100  
SMOKE_AVOIDANCE_STRENGTH = 1
SMOKE_DAMAGE_RATE = 0.5
HEAT_DAMAGE_RATE = 70

# Window configuration
WIDTH, HEIGHT = 1600, 1000
BACKGROUND_COLOR = (30, 30, 30)
WALL_COLOR = (100, 100, 100)
EXIT_COLOR = (0, 255, 100)
DOOR_COLOR = (200, 200, 0)

# Boid parameters
NUM_BOIDS = 500
BOID_RADIUS = 5
BOID_COLOR = (100, 200, 255)
ALIGNMENT_STRENGTH = 0.05
COHESION_STRENGTH = 0.01
SEPARATION_STRENGTH = 1
WALL_AVOIDANCE_STRENGTH = 0.1
EXIT_STRENGTH = 1.5
MAX_SPEED = 2.5
VISION_RADIUS = 150
WALL_DETECTION_DISTANCE = 30
EXIT_PASS_DISTANCE = 10
CHANCE_TO_STOP = 0.0
CHANCE_TO_CHANGE_DIRECTION = 0.5

#Fire and smoke parameters
HEAT_DAMAGE_RATE = 0.2
HEALTH_RECOVERY_RATE = 0.05
FIRE_AVOIDANCE_RADIUS = 100
FIRE_AVOIDANCE_STRENGTH = 2.0
SMOKE_SLOWDOWN_FACTOR = 0.5


# Wall thickness
WALL_THICKNESS = 10

# Base coordinates for alignment
BASE_X = 300
BASE_Y = 100
ROOM_HEIGHT = 200
MAIN_ROOM_HEIGHT = 300
ROOM_WIDTH = 200
MAIN_ROOM_WIDTH = 400


ROOMS = {
    # Grande salle centrale (1)
    1: {
        "bounds": (BASE_X + ROOM_WIDTH, BASE_Y + ROOM_HEIGHT, MAIN_ROOM_WIDTH, MAIN_ROOM_HEIGHT),
        "spawn_area": (BASE_X + ROOM_WIDTH + 20, BASE_Y + ROOM_HEIGHT + 20, MAIN_ROOM_WIDTH - 40, MAIN_ROOM_HEIGHT - 40),
        "exits": [
            {
                "id": 1,
                "to_room": 2,
                "position": (BASE_X + ROOM_WIDTH + WALL_THICKNESS//2, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT//2),
                "spawn_point": (BASE_X + ROOM_WIDTH - 20, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT//2),
                "direction": (-1, 0),
                "flow_rate": 2,
                "width": 40
            },
            {
                "id": 2,
                "to_room": 3,
                "position": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH - WALL_THICKNESS//2, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT//2),
                "spawn_point": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH + 20, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT//2),
                "direction": (1, 0),
                "flow_rate": 2,
                "width": 40
            },
            {
                "id": 3,
                "to_room": 4,
                "position": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH//2, BASE_Y + ROOM_HEIGHT + WALL_THICKNESS//2),
                "spawn_point": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH//2, BASE_Y + ROOM_HEIGHT - 20),
                "direction": (0, -1),
                "flow_rate": 2,
                "width": 40
            },
            {
                "id": 4,
                "to_room": 7,
                "position": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH//2, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT - WALL_THICKNESS//2),
                "spawn_point": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH//2, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + 20),
                "direction": (0, 1),
                "flow_rate": 2,
                "width": 40
            }
        ]
    },
    # Couloir Ouest (2)
    2: {
        "bounds": (BASE_X, BASE_Y + ROOM_HEIGHT, ROOM_WIDTH, MAIN_ROOM_HEIGHT),
        "spawn_area": (BASE_X + 20, BASE_Y + ROOM_HEIGHT + 20, ROOM_WIDTH - 40, MAIN_ROOM_HEIGHT - 40),
        "exits": [
            {
                "id": 5,
                "to_room": 5,
                "position": (BASE_X + ROOM_WIDTH//2, BASE_Y + ROOM_HEIGHT + WALL_THICKNESS//2),
                "spawn_point": (BASE_X + ROOM_WIDTH//2, BASE_Y + ROOM_HEIGHT - 20),
                "direction": (0, -1),
                "flow_rate": 2,
                "width": 40
            },
            {
                "id": 6,
                "to_room": 6,
                "position": (BASE_X + ROOM_WIDTH//2, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT - WALL_THICKNESS//2),
                "spawn_point": (BASE_X + ROOM_WIDTH//2, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + 20),
                "direction": (0, 1),
                "flow_rate": 2,
                "width": 40
            }
        ]
    },
    # Couloir Est (3)
    3: {
        "bounds": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH, BASE_Y + ROOM_HEIGHT, ROOM_WIDTH, MAIN_ROOM_HEIGHT),
        "spawn_area": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH + 20, BASE_Y + ROOM_HEIGHT + 20, ROOM_WIDTH - 40, MAIN_ROOM_HEIGHT - 40),
        "exits": [
            {
                "id": 7,
                "to_room": 8,
                "position": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH + ROOM_WIDTH//2, BASE_Y + ROOM_HEIGHT + WALL_THICKNESS//2),
                "spawn_point": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH + ROOM_WIDTH//2, BASE_Y + ROOM_HEIGHT - 20),
                "direction": (0, -1),
                "flow_rate": 2,
                "width": 40
            },
            {
                "id": 8,
                "to_room": 9,
                "position": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH + ROOM_WIDTH//2, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT - WALL_THICKNESS//2),
                "spawn_point": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH + ROOM_WIDTH//2, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + 20),
                "direction": (0, 1),
                "flow_rate": 2,
                "width": 40
            }
        ]
    },
    # Salle Nord (4)
    4: {
        "bounds": (BASE_X + ROOM_WIDTH, BASE_Y, MAIN_ROOM_WIDTH, ROOM_HEIGHT),
        "spawn_area": (BASE_X + ROOM_WIDTH + 20, BASE_Y + 20, MAIN_ROOM_WIDTH - 40, ROOM_HEIGHT - 40),
        "exits": [
            {
                "id": 9,
                "to_room": 5,
                "position": (BASE_X + ROOM_WIDTH + WALL_THICKNESS//2, BASE_Y + ROOM_HEIGHT//2),
                "spawn_point": (BASE_X + ROOM_WIDTH - 20, BASE_Y + ROOM_HEIGHT//2),
                "direction": (-1, 0),
                "flow_rate": 2,
                "width": 40
            },
            {
                "id": 10,
                "to_room": 8,
                "position": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH - WALL_THICKNESS//2, BASE_Y + ROOM_HEIGHT//2),
                "spawn_point": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH + 20, BASE_Y + ROOM_HEIGHT//2),
                "direction": (1, 0),
                "flow_rate": 2,
                "width": 40
            }
        ]
    },
    # Les autres salles suivent le même modèle...
    # Salle Nord-Ouest (5)
    5: {
        "bounds": (BASE_X, BASE_Y, ROOM_WIDTH, ROOM_HEIGHT),
        "spawn_area": (BASE_X + 20, BASE_Y + 20, ROOM_WIDTH - 40, ROOM_HEIGHT - 40),
        "exits": [
            {
                "id": 11,
                "to_room": None,
                "position": (BASE_X + WALL_THICKNESS//2, BASE_Y + ROOM_HEIGHT//2),
                "spawn_point": None,
                "direction": (-1, 0),
                "flow_rate": 3,
                "width": 40
            }
        ]
    },
    # Salle Sud-Ouest (6)
    6: {
        "bounds": (BASE_X, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT, ROOM_WIDTH, ROOM_HEIGHT),
        "spawn_area": (BASE_X + 20, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + 20, ROOM_WIDTH - 40, ROOM_HEIGHT - 40),
        "exits": [
            {
                "id": 12,
                "to_room": None,
                "position": (BASE_X + WALL_THICKNESS//2, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + ROOM_HEIGHT//2),
                "spawn_point": None,
                "direction": (-1, 0),
                "flow_rate": 3,
                "width": 40
            }
        ]
    },
    # Salle Sud (7)
    7: {
        "bounds": (BASE_X + ROOM_WIDTH, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT, MAIN_ROOM_WIDTH, ROOM_HEIGHT),
        "spawn_area": (BASE_X + ROOM_WIDTH + 20, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + 20, MAIN_ROOM_WIDTH - 40, ROOM_HEIGHT - 40),
        "exits": [
            {
                "id": 13,
                "to_room": 6,
                "position": (BASE_X + ROOM_WIDTH + WALL_THICKNESS//2, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + ROOM_HEIGHT//2),
                "spawn_point": (BASE_X + ROOM_WIDTH - 20, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + ROOM_HEIGHT//2),
                "direction": (-1, 0),
                "flow_rate": 2,
                "width": 40
            },
            {
                "id": 14,
                "to_room": 9,
                "position": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH - WALL_THICKNESS//2, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + ROOM_HEIGHT//2),
                "spawn_point": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH + 20, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + ROOM_HEIGHT//2),
                "direction": (1, 0),
                "flow_rate": 2,
                "width": 40
            }
        ]
    },
    # Salle Nord-Est (8)
    8: {
        "bounds": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH, BASE_Y, ROOM_WIDTH, ROOM_HEIGHT),
        "spawn_area": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH + 20, BASE_Y + 20, ROOM_WIDTH - 40, ROOM_HEIGHT - 40),
        "exits": [
            {
                "id": 15,
                "to_room": None,
                "position": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH + ROOM_WIDTH - WALL_THICKNESS//2, BASE_Y + ROOM_HEIGHT//2),
                "spawn_point": None,
                "direction": (1, 0),
                "flow_rate": 3,
                "width": 40
            }
        ]
    },
    # Salle Sud-Est (9)
    9: {
        "bounds": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT, ROOM_WIDTH, ROOM_HEIGHT),
        "spawn_area": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH + 20, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + 20, ROOM_WIDTH - 40, ROOM_HEIGHT - 40),
        "exits": [
            {
                "id": 16,
                "to_room": None,
                "position": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH + ROOM_WIDTH - WALL_THICKNESS//2, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + ROOM_HEIGHT//2),
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
    id: 500 for id in range(1, 17)  # 500ms (2 boids/sec) for all exits
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

# Définition des obstacles
OBSTACLES = [
    # Salle centrale
    pygame.Rect(BASE_X + ROOM_WIDTH + 100, BASE_Y + ROOM_HEIGHT + 100, 30, 30),  # Petit carré
    pygame.Rect(BASE_X + ROOM_WIDTH + 300, BASE_Y + ROOM_HEIGHT + 150, 50, 20),  # Rectangle horizontal
    pygame.Rect(BASE_X + ROOM_WIDTH + 200, BASE_Y + ROOM_HEIGHT + 200, 20, 50),  # Rectangle vertical
    
    # Obstacles additionnels dans la salle centrale
    pygame.Rect(BASE_X + ROOM_WIDTH + 150, BASE_Y + ROOM_HEIGHT + 50, 40, 40),   # Carré en haut
    pygame.Rect(BASE_X + ROOM_WIDTH + 320, BASE_Y + ROOM_HEIGHT + 220, 60, 25),  # Rectangle en bas droite
    
    # Salle Nord (4)
    pygame.Rect(BASE_X + ROOM_WIDTH + 150, BASE_Y + 20, 25, 60),  # Rectangle vertical
    pygame.Rect(BASE_X + ROOM_WIDTH + 300, BASE_Y + 50, 60, 25),  # Rectangle horizontal
    
    # Salle Sud (7)
    pygame.Rect(BASE_X + ROOM_WIDTH + 180, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + 30, 30, 40),
    pygame.Rect(BASE_X + ROOM_WIDTH + 280, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + 70, 40, 30),
    
    # Couloir Ouest (2)
    pygame.Rect(BASE_X + 20, BASE_Y + ROOM_HEIGHT + 150, 30, 80),
    pygame.Rect(BASE_X + 120, BASE_Y + ROOM_HEIGHT + 250, 60, 25),
    
    # Couloir Est (3)
    pygame.Rect(BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH + 50, BASE_Y + ROOM_HEIGHT + 100, 25, 60),
    pygame.Rect(BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH + 100, BASE_Y + ROOM_HEIGHT + 200, 60, 25),
    
    # Salles périphériques
    # Nord-Ouest (5)
    pygame.Rect(BASE_X + 50, BASE_Y + 50, 40, 40),
    
    # Nord-Est (8)
    pygame.Rect(BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH + 50, BASE_Y + 50, 40, 40),
    
    # Sud-Ouest (6)
    pygame.Rect(BASE_X + 50, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + 50, 40, 40),
    
    # Sud-Est (9)
    pygame.Rect(BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH + 50, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + 50, 40, 40)
]

# Ajouter les obstacles aux murs
WALLS.extend(OBSTACLES)



# # Configuration des murs et pièces
# WALL_THICKNESS = 10
# BASE_X = 300
# BASE_Y = 100
# ROOM_HEIGHT = 200
# MAIN_ROOM_HEIGHT = 300
# ROOM_WIDTH = 200
# MAIN_ROOM_WIDTH = 400

# ROOMS = {
#     # Grande salle centrale (1)
#     1: {
#         "name": "Grande salle centrale",
#         "type": "main",
#         "bounds": (BASE_X + ROOM_WIDTH, BASE_Y + ROOM_HEIGHT, MAIN_ROOM_WIDTH, MAIN_ROOM_HEIGHT),
#         "spawn_area": (BASE_X + ROOM_WIDTH + 20, BASE_Y + ROOM_HEIGHT + 20, MAIN_ROOM_WIDTH - 40, MAIN_ROOM_HEIGHT - 40),
#         "exits": [
#             {
#                 "id": 1,
#                 "to_room": 2,
#                 "position": (BASE_X + ROOM_WIDTH + WALL_THICKNESS//2, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT//2),
#                 "spawn_point": (BASE_X + ROOM_WIDTH - 20, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT//2),
#                 "direction": (-1, 0),
#                 "flow_rate": 2,
#                 "width": 40
#             },
#             {
#                 "id": 3,
#                 "to_room": 4,
#                 "position": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH//2, BASE_Y + ROOM_HEIGHT + WALL_THICKNESS//2),
#                 "spawn_point": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH//2, BASE_Y + ROOM_HEIGHT - 20),
#                 "direction": (0, -1),
#                 "flow_rate": 2,
#                 "width": 40
#             },
#             {
#                 "id": 4,
#                 "to_room": 7,
#                 "position": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH//2, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT - WALL_THICKNESS//2),
#                 "spawn_point": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH//2, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + 20),
#                 "direction": (0, 1),
#                 "flow_rate": 2,
#                 "width": 40
#             }
#         ]
#     },
#     # Couloir Ouest (2)
#     2: {
#         "name": "Couloir Ouest",
#         "type": "corridor",
#         "bounds": (BASE_X, BASE_Y + ROOM_HEIGHT, ROOM_WIDTH, MAIN_ROOM_HEIGHT),
#         "spawn_area": (BASE_X + 20, BASE_Y + ROOM_HEIGHT + 20, ROOM_WIDTH - 40, MAIN_ROOM_HEIGHT - 40),
#         "exits": [
#             {
#                 "id": 5,
#                 "to_room": 5,
#                 "position": (BASE_X + ROOM_WIDTH//2, BASE_Y + ROOM_HEIGHT + WALL_THICKNESS//2),
#                 "spawn_point": (BASE_X + ROOM_WIDTH//2, BASE_Y + ROOM_HEIGHT - 20),
#                 "direction": (0, -1),
#                 "flow_rate": 2,
#                 "width": 40
#             },
#             {
#                 "id": 6,
#                 "to_room": 6,
#                 "position": (BASE_X + ROOM_WIDTH//2, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT - WALL_THICKNESS//2),
#                 "spawn_point": (BASE_X + ROOM_WIDTH//2, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + 20),
#                 "direction": (0, 1),
#                 "flow_rate": 2,
#                 "width": 40
#             }
#         ]
#     },
#     # Couloir Est (3)
#     3: {
#         "name": "Couloir Est",
#         "type": "corridor",
#         "bounds": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH, BASE_Y + ROOM_HEIGHT, ROOM_WIDTH, MAIN_ROOM_HEIGHT),
#         "spawn_area": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH + 20, BASE_Y + ROOM_HEIGHT + 20, ROOM_WIDTH - 40, MAIN_ROOM_HEIGHT - 40),
#         "exits": [
#             {
#                 "id": 7,  # ID unique
#                 "to_room": 1,
#                 "position": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH - WALL_THICKNESS//2, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT//2),
#                 "spawn_point": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH - 20, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT//2),
#                 "direction": (-1, 0),  # Vers la gauche pour rejoindre la salle centrale
#                 "flow_rate": 2,
#                 "width": 40
#             }
#         ]
#     },
#     # Salle Nord (4)
#     4: {
#         "name": "Salle Nord",
#         "type": "room",
#         "bounds": (BASE_X + ROOM_WIDTH, BASE_Y, MAIN_ROOM_WIDTH, ROOM_HEIGHT),
#         "spawn_area": (BASE_X + ROOM_WIDTH + 20, BASE_Y + 20, MAIN_ROOM_WIDTH - 40, ROOM_HEIGHT - 40),
#         "exits": [
#             {
#                 "id": 8,
#                 "to_room": None,
#                 "position": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH//2, BASE_Y + WALL_THICKNESS//2),
#                 "spawn_point": None,
#                 "direction": (0, -1),
#                 "flow_rate": 3,
#                 "width": 40
#             }
#         ]
#     },
#     # Salle Nord-Ouest (5)
#     5: {
#         "name": "Salle Nord-Ouest",
#         "type": "room",
#         "bounds": (BASE_X, BASE_Y, ROOM_WIDTH, ROOM_HEIGHT),
#         "spawn_area": (BASE_X + 20, BASE_Y + 20, ROOM_WIDTH - 40, ROOM_HEIGHT - 40),
#         "exits": [
#             {
#                 "id": 9,
#                 "to_room": None,
#                 "position": (BASE_X + WALL_THICKNESS//2, BASE_Y + ROOM_HEIGHT//2),
#                 "spawn_point": None,
#                 "direction": (-1, 0),
#                 "flow_rate": 3,
#                 "width": 40
#             }
#         ]
#     },
#     # Salle Sud-Ouest (6)
#     6: {
#         "name": "Salle Sud-Ouest",
#         "type": "room",
#         "bounds": (BASE_X, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT, ROOM_WIDTH, ROOM_HEIGHT),
#         "spawn_area": (BASE_X + 20, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + 20, ROOM_WIDTH - 40, ROOM_HEIGHT - 40),
#         "exits": [
#             {
#                 "id": 10,
#                 "to_room": None,
#                 "position": (BASE_X + WALL_THICKNESS//2, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + ROOM_HEIGHT//2),
#                 "spawn_point": None,
#                 "direction": (-1, 0),
#                 "flow_rate": 3,
#                 "width": 40
#             }
#         ]
#     },
#     # Salle Sud (7)
#     7: {
#         "name": "Salle Sud",
#         "type": "room",
#         "bounds": (BASE_X + ROOM_WIDTH, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT, MAIN_ROOM_WIDTH, ROOM_HEIGHT),
#         "spawn_area": (BASE_X + ROOM_WIDTH + 20, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + 20, MAIN_ROOM_WIDTH - 40, ROOM_HEIGHT - 40),
#         "exits": [
#             {
#                 "id": 11,
#                 "to_room": None,
#                 "position": (BASE_X + ROOM_WIDTH + MAIN_ROOM_WIDTH//2, BASE_Y + ROOM_HEIGHT + MAIN_ROOM_HEIGHT + ROOM_HEIGHT - WALL_THICKNESS//2),
#                 "spawn_point": None,
#                 "direction": (0, 1),
#                 "flow_rate": 3,
#                 "width": 40
#             }
#         ]
#     }
# }

# # Configuration des files d'attente des sorties
# EXIT_QUEUE_MAX_SIZE = 5
# EXIT_PROCESSING_TIME = {id: 500 for id in range(1, 12)}  # 500ms pour toutes les sorties

# # Génération des murs basée sur les définitions des pièces
# WALLS = []
# for room_id, room in ROOMS.items():
#     x, y, w, h = room["bounds"]
#     WALLS.extend([
#         pygame.Rect(x, y, w, WALL_THICKNESS),  # Haut
#         pygame.Rect(x, y + h, w, WALL_THICKNESS),  # Bas
#         pygame.Rect(x, y, WALL_THICKNESS, h),  # Gauche
#         pygame.Rect(x + w, y, WALL_THICKNESS, h)  # Droite
#     ])