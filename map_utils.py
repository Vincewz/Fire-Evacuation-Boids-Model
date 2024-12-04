import pygame
from config import *
import numpy as np
class Map:
    def __init__(self):
        self.walls = WALLS
        self.rooms = ROOMS

    def draw(self, screen):
        # Draw rooms
        for room_id, room in self.rooms.items():
            bounds = room["bounds"]
            pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(*bounds), 1)
            
            # Draw exits for this room
            for exit_info in room["exits"]:
                pos = exit_info["position"]
                width = exit_info["width"]
                pygame.draw.circle(screen, EXIT_COLOR, pos, width//2, 1)

        # Draw walls
        for wall in self.walls:
            pygame.draw.rect(screen, WALL_COLOR, wall)

    def is_point_in_wall(self, point):
        """Check if a point is inside any wall using NumPy."""
        # Ensure point is a NumPy array
        point = np.array(point, dtype=float)

        # Check for NaN values in point
        if np.any(np.isnan(point)):
            return False

        return any(wall.collidepoint(int(point[0]), int(point[1])) for wall in self.walls)

    def get_wall_avoidance_force(self, position):
        """Calculate the force to avoid walls using NumPy."""
        avoidance = np.array([0.0, 0.0], dtype=float)
        pos = np.array(position, dtype=float)

        for wall in self.walls:
            # Find closest point on the wall using NumPy
            closest_x = np.clip(pos[0], wall.left, wall.right)
            closest_y = np.clip(pos[1], wall.top, wall.bottom)
            closest_point = np.array([closest_x, closest_y], dtype=float)

            # Calculate the distance to the closest point on the wall
            distance = np.linalg.norm(pos - closest_point)

            # If the boid is close enough to the wall, calculate the avoidance force
            if distance < WALL_DETECTION_DISTANCE and distance > 0:
                # Calculate force vector (avoidance direction)
                force = (pos - closest_point) / distance
                avoidance += force * (1 - distance / WALL_DETECTION_DISTANCE)

        return avoidance
