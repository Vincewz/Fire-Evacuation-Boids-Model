import numpy as np
import pygame 
import random
from config import *

class FireManager:
    def __init__(self, rooms):
        self.rooms = rooms
        self.Nx = WIDTH // 4
        self.Ny = HEIGHT // 4
        self.dx = WIDTH / self.Nx
        self.dy = HEIGHT / self.Ny
        
        # Grille de fumée
        self.smoke_concentration = np.zeros((self.Ny, self.Nx))
        # Grille des murs (True = mur ou sortie extérieure, False = passage possible)
        self.wall_grid = np.zeros((self.Ny, self.Nx), dtype=bool)
        self.init_grids()
        
        # Point de départ du feu
        self.fire_source = None
        self.init_first_fire()
        
        # Paramètres
        self.propagation_chance = 0.3
        self.smoke_increment = 0.2
        self.dissipation_rate = 0.02

    def init_grids(self):
        """Initialise la grille des murs en laissant des passages uniquement aux portes intérieures"""
        # D'abord marquer tous les murs
        for wall in WALLS:
            x1 = max(0, min(self.Nx - 1, int(wall.left / self.dx)))
            x2 = max(0, min(self.Nx - 1, int(wall.right / self.dx)))
            y1 = max(0, min(self.Ny - 1, int(wall.top / self.dy)))
            y2 = max(0, min(self.Ny - 1, int(wall.bottom / self.dy)))
            self.wall_grid[y1:y2+1, x1:x2+1] = True
        
        # Créer des passages uniquement aux portes intérieures
        for room in self.rooms.values():
            for exit_info in room["exits"]:
                # Si c'est une sortie vers l'extérieur (to_room est None), ne pas créer de passage
                if exit_info["to_room"] is None:
                    continue
                    
                # Convertir la position de la porte en indices de grille
                door_x = int(exit_info["position"][0] / self.dx)
                door_y = int(exit_info["position"][1] / self.dy)
                
                # Créer une ouverture dans le mur
                door_width = max(1, int(exit_info["width"] / (2 * self.dx)))
                for dx in range(-door_width, door_width + 1):
                    for dy in range(-door_width, door_width + 1):
                        grid_x = door_x + dx
                        grid_y = door_y + dy
                        if 0 <= grid_x < self.Nx and 0 <= grid_y < self.Ny:
                            self.wall_grid[grid_y, grid_x] = False

    def init_first_fire(self):
        room_id = random.choice(list(self.rooms.keys()))
        room = self.rooms[room_id]
        
        bounds = room["spawn_area"]
        x = random.randint(bounds[0], bounds[0] + bounds[2])
        y = random.randint(bounds[1], bounds[1] + bounds[3])
        
        self.fire_source = (int(x / self.dx), int(y / self.dy))
        self.smoke_concentration[self.fire_source[1], self.fire_source[0]] = 1.0

    def update(self):
        new_smoke = np.copy(self.smoke_concentration)
        
        # Ajouter constamment de la fumée à la source
        if self.fire_source:
            new_smoke[self.fire_source[1], self.fire_source[0]] = 1.0
        
        # Propager la fumée
        for i in range(1, self.Nx-1):
            for j in range(1, self.Ny-1):
                if self.wall_grid[j,i]:
                    new_smoke[j,i] = 0
                    continue
                
                if self.smoke_concentration[j,i] > 0.1:
                    # Directions possibles de propagation
                    directions = [(0,1), (0,-1), (1,0), (-1,0)]
                    
                    for dx, dy in directions:
                        new_x, new_y = i + dx, j + dy
                        
                        if (0 <= new_x < self.Nx and 0 <= new_y < self.Ny 
                            and not self.wall_grid[new_y,new_x]):
                            
                            if random.random() < self.propagation_chance:
                                new_value = min(1.0, new_smoke[new_y,new_x] + self.smoke_increment)
                                new_smoke[new_y,new_x] = new_value
                
                # Dissipation naturelle
                new_smoke[j,i] = max(0, new_smoke[j,i] - self.dissipation_rate)
        
        self.smoke_concentration = new_smoke

    def get_smoke_at_position(self, x, y):
        grid_x = int(x / self.dx)
        grid_y = int(y / self.dy)
        if 0 <= grid_x < self.Nx and 0 <= grid_y < self.Ny:
            return self.smoke_concentration[grid_y, grid_x]
        return 0

    def get_temperature_at_position(self, x, y):
        grid_x = int(x / self.dx)
        grid_y = int(y / self.dy)
        if (grid_x, grid_y) == self.fire_source:
            return 1.0
        return 0

    def draw(self, screen):
        smoke_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        for i in range(self.Nx):
            for j in range(self.Ny):
                value = self.smoke_concentration[j,i]
                if value > 0.01:
                    alpha = int(180 * value)
                    color = (100, 100, 100, alpha)
                    pygame.draw.rect(smoke_surf, color,
                                   (i*self.dx, j*self.dy, self.dx+1, self.dy+1))
        
        screen.blit(smoke_surf, (0, 0))
        
        if self.fire_source:
            x = int(self.fire_source[0] * self.dx)
            y = int(self.fire_source[1] * self.dy)
            pygame.draw.circle(screen, (255, 0, 0), (x, y), 5)