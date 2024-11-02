import pygame
from config import *

class Map:
    def __init__(self):
        self.walls = WALL
        self.exits = sorted(EXITS, key=lambda x: x["order"])

    def draw(self, screen):
        # Draw walls
        for wall in self.walls:
            pygame.draw.rect(screen, WALL_COLOR, wall)
            
        # Draw exits
        for idx, exit_info in enumerate(self.exits):
            color = (0, 255 - idx * 50, 0)  # Different color for each exit
            pygame.draw.circle(screen, color, exit_info["attraction_point"], 5)
            
            # Draw exit number
            font = pygame.font.Font(None, 24)
            text = font.render(str(exit_info["order"]), True, (255, 255, 255))
            screen.blit(text, (exit_info["attraction_point"][0] - 5, 
                              exit_info["attraction_point"][1] - 20))

    def get_nearest_exit_point(self, position, exits_passed):
        # Get next exit in sequence that hasn't been passed
        for exit_info in self.exits:
            if exit_info["id"] not in exits_passed:
                return pygame.Vector2(exit_info["attraction_point"]), exit_info["id"]
        return None, None

    def is_point_in_wall(self, point):
        return any(wall.collidepoint(point) for wall in self.walls)

    def get_wall_avoidance_force(self, position):
        avoidance = pygame.Vector2(0, 0)
        pos = pygame.Vector2(position)
        
        for wall in self.walls:
            closest_x = max(wall.left, min(pos.x, wall.right))
            closest_y = max(wall.top, min(pos.y, wall.bottom))
            closest_point = pygame.Vector2(closest_x, closest_y)
            
            distance = pos.distance_to(closest_point)
            if distance < WALL_DETECTION_DISTANCE:
                if distance > 0:
                    force = (pos - closest_point) / distance
                    avoidance += force * (1 - distance / WALL_DETECTION_DISTANCE)
                
        return avoidance