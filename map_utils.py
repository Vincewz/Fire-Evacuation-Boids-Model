import pygame
from config import *

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
        """Check if a point is inside any wall."""
        if isinstance(point, pygame.Vector2):
            return any(wall.collidepoint(int(point.x), int(point.y)) for wall in self.walls)
        return any(wall.collidepoint(int(point[0]), int(point[1])) for wall in self.walls)

    def get_wall_avoidance_force(self, position):
        """Calculate the force to avoid walls."""
        avoidance = pygame.Vector2(0, 0)
        pos = pygame.Vector2(position)
        
        for wall in self.walls:
            # Find closest point on wall
            closest_x = max(wall.left, min(pos.x, wall.right))
            closest_y = max(wall.top, min(pos.y, wall.bottom))
            closest_point = pygame.Vector2(closest_x, closest_y)
            
            # Calculate distance to wall
            distance = pos.distance_to(closest_point)
            
            # If boid is close enough to wall, calculate avoidance force
            if distance < WALL_DETECTION_DISTANCE and distance > 0:
                force = (pos - closest_point) / distance
                avoidance += force * (1 - distance / WALL_DETECTION_DISTANCE)
                
        return avoidance