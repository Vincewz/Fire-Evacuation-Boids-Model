import pygame
from config import *

class Map:
    def __init__(self):
        self.walls = WALLS
        self.rooms = ROOMS
        # Grid size matching the smoke simulation grid
        self.grid_size = 4  # Since FireManager uses WIDTH // 4
        self.init_wall_grid()

    def is_line_of_sight_clear(self, start_pos, end_pos):
        """Vérifie si la ligne de vue entre deux points est dégagée"""
        # Nombre de points à vérifier sur la ligne
        num_points = 10
        
        # Vérifier plusieurs points le long de la ligne
        for i in range(num_points):
            t = i / (num_points - 1)
            check_x = start_pos.x + (end_pos.x - start_pos.x) * t
            check_y = start_pos.y + (end_pos.y - start_pos.y) * t
            
            # Si un point est dans un mur, la ligne de vue est bloquée
            if self.is_point_in_wall(pygame.Vector2(check_x, check_y)):
                return False
                
        return True

    def init_wall_grid(self):
        """Initialize wall grid aligned with smoke grid"""
        self.grid_width = WIDTH // self.grid_size
        self.grid_height = HEIGHT // self.grid_size
        self.wall_grid = [[False for x in range(self.grid_width)] for y in range(self.grid_height)]
        
        # Convert walls to grid
        for wall in self.walls:
            grid_left = max(0, wall.left // self.grid_size)
            grid_right = min(self.grid_width - 1, (wall.right // self.grid_size) + 1)
            grid_top = max(0, wall.top // self.grid_size)
            grid_bottom = min(self.grid_height - 1, (wall.bottom // self.grid_size) + 1)
            
            for y in range(grid_top, grid_bottom):
                for x in range(grid_left, grid_right):
                    self.wall_grid[y][x] = True

    def draw(self, screen):
        # Draw rooms
        for room_id, room in self.rooms.items():
            bounds = room["bounds"]
            pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(*bounds), 1)
            
            # Draw exits
            for exit_info in room["exits"]:
                pos = exit_info["position"]
                width = exit_info["width"]
                pygame.draw.circle(screen, EXIT_COLOR, pos, width//2, 1)

        # Draw walls
        for wall in self.walls:
            pygame.draw.rect(screen, WALL_COLOR, wall)

    def is_point_in_wall(self, point):
        """Check if a point is inside any wall using the grid"""
        grid_x = int(point.x // self.grid_size)
        grid_y = int(point.y // self.grid_size)
        
        # Add a small margin to prevent boids from getting too close to walls
        margin = 1
        for dy in range(-margin, margin + 1):
            for dx in range(-margin, margin + 1):
                check_x = grid_x + dx
                check_y = grid_y + dy
                if (0 <= check_x < self.grid_width and 
                    0 <= check_y < self.grid_height and 
                    self.wall_grid[check_y][check_x]):
                    return True
        return False

    def get_wall_avoidance_force(self, position):
        """Calculate the force to avoid walls using the grid"""
        avoidance = pygame.Vector2(0, 0)
        grid_x = int(position.x // self.grid_size)
        grid_y = int(position.y // self.grid_size)
        
        check_radius = WALL_DETECTION_DISTANCE // self.grid_size
        pos = pygame.Vector2(position)
        
        for dy in range(-check_radius, check_radius + 1):
            for dx in range(-check_radius, check_radius + 1):
                check_x = grid_x + dx
                check_y = grid_y + dy
                
                if (0 <= check_x < self.grid_width and 
                    0 <= check_y < self.grid_height and 
                    self.wall_grid[check_y][check_x]):
                    
                    wall_center = pygame.Vector2(
                        (check_x + 0.5) * self.grid_size,
                        (check_y + 0.5) * self.grid_size
                    )
                    
                    distance = pos.distance_to(wall_center)
                    if 0 < distance < WALL_DETECTION_DISTANCE:
                        force = (pos - wall_center) / distance
                        avoidance += force * (1 - distance / WALL_DETECTION_DISTANCE)
        
        return avoidance