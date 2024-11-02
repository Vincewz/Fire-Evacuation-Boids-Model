import pygame

# Window configuration
WIDTH, HEIGHT = 1200, 800
BACKGROUND_COLOR = (30, 30, 30)
WALL_COLOR = (100, 100, 100)
EXIT_COLOR = (0, 255, 100)
DOOR_COLOR = (200, 200, 0)

# Boid parameters
NUM_BOIDS = 10  # Nombre de boids
BOID_RADIUS = 5
BOID_COLOR = (100, 200, 255)
ALIGNMENT_STRENGTH = 0.05
COHESION_STRENGTH = 0.01
SEPARATION_STRENGTH = 0.05
WALL_AVOIDANCE_STRENGTH = 0.15
EXIT_STRENGTH = 0.3
MAX_SPEED = 2
VISION_RADIUS = 50
WALL_DETECTION_DISTANCE = 30
EXIT_PASS_DISTANCE = 10  # Distance à laquelle une sortie est considérée comme atteinte

# Wall thickness
WALL_THICKNESS = 10

# Define wall (x, y, width, height)
WALL = [
    # Main room
    pygame.Rect(100, 100, 400, 5), #TOP
    pygame.Rect(100, 100, 5, 400), #LEFT
    pygame.Rect(500, 100, 5, 50), #Right 1
    pygame.Rect(500, 160, 5, 380), #Right 2
    pygame.Rect(100, 500, 400, 5), #Bottom
    #Second room
    pygame.Rect(500, 100, 200, 5), #TOP
    pygame.Rect(700, 100, 5, 500), #Right
    pygame.Rect(500, 560, 5, 40), #Left 1
    pygame.Rect(200, 600, 505, 5), #botoom

]

# Define exits with order
EXITS = [
    {"id": 1, "attraction_point": (507, 150), "order": 1},
    {"id": 2, "attraction_point": (500, 550), "order": 2},
    {"id": 3, "attraction_point": (100, 600), "order": 3},
]