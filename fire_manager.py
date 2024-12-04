import numpy as np
import pygame
import random
from config import *
import math

class FireManager:
    def __init__(self, rooms):
        self.rooms = rooms
        # Grille plus fine pour une meilleure simulation de fumée
        self.Nx = WIDTH // 4
        self.Ny = HEIGHT // 4
        self.dx = WIDTH / self.Nx
        self.dy = HEIGHT / self.Ny
        self.dt = 2.0
        self.D = 8.0  # Coefficient de diffusion augmenté pour compenser l'absence de vent
        
        # Grilles
        self.smoke_concentration = np.zeros((self.Ny, self.Nx))
        self.temperature = np.zeros((self.Ny, self.Nx))
        
        # Création de la grille des murs
        self.wall_grid = np.zeros((self.Ny, self.Nx), dtype=bool)
        self.init_wall_grid()
        
        # Sources de feu fixes
        self.fire_sources = []
        self.init_first_fire()

    def init_wall_grid(self):
        """Initialise la grille des murs pour la simulation de fumée"""
        for wall in WALLS:
            x1 = max(0, min(self.Nx - 1, int(wall.left / self.dx)))
            x2 = max(0, min(self.Nx - 1, int(wall.right / self.dx)))
            y1 = max(0, min(self.Ny - 1, int(wall.top / self.dy)))
            y2 = max(0, min(self.Ny - 1, int(wall.bottom / self.dy)))
            self.wall_grid[y1:y2+1, x1:x2+1] = True

    def init_first_fire(self):
        """Initialise un feu dans une position aléatoire"""
        room_id = random.choice(list(self.rooms.keys()))
        room = self.rooms[room_id]
        
        bounds = room["spawn_area"]
        x = random.randint(bounds[0], bounds[0] + bounds[2])
        y = random.randint(bounds[1], bounds[1] + bounds[3])
        
        grid_x = int(x / self.dx)
        grid_y = int(y / self.dy)
        
        self.fire_sources.append((grid_x, grid_y, 2.0, 0))

    def add_fire_smoke(self):
        """Ajoute de la fumée pour chaque source de feu"""
        radius = 4
        for fire_x, fire_y, strength, _ in self.fire_sources:
            for i in range(fire_x-radius, fire_x+radius+1):
                for j in range(fire_y-radius, fire_y+radius+1):
                    if 0 <= i < self.Nx and 0 <= j < self.Ny and not self.wall_grid[j,i]:
                        dist = np.sqrt((i-fire_x)**2 + (j-fire_y)**2)
                        if dist < radius:
                            self.smoke_concentration[j,i] = min(1.0, 
                                self.smoke_concentration[j,i] + strength * (1 - dist/radius))
                            self.temperature[j,i] = strength

    def update(self):
        """Met à jour la simulation de fumée - diffusion uniquement"""
        self.add_fire_smoke()
        
        # Diffusion de la fumée
        smoke_new = np.copy(self.smoke_concentration)
        
        for i in range(1, self.Nx-1):
            for j in range(1, self.Ny-1):
                if self.wall_grid[j,i]:
                    smoke_new[j,i] = 0
                    continue
                    
                # Vérifier les murs voisins pour la diffusion
                can_diffuse_left = not self.wall_grid[j,i-1]
                can_diffuse_right = not self.wall_grid[j,i+1]
                can_diffuse_up = not self.wall_grid[j-1,i]
                can_diffuse_down = not self.wall_grid[j+1,i]
                
                # Diffusion (propagation naturelle)
                diff_x = diff_y = 0
                if can_diffuse_left and can_diffuse_right:
                    diff_x = self.D * (self.smoke_concentration[j,i+1] - 2*self.smoke_concentration[j,i] + 
                                     self.smoke_concentration[j,i-1])/self.dx**2
                if can_diffuse_up and can_diffuse_down:
                    diff_y = self.D * (self.smoke_concentration[j+1,i] - 2*self.smoke_concentration[j,i] + 
                                     self.smoke_concentration[j-1,i])/self.dy**2
                
                # Mise à jour avec la diffusion uniquement
                smoke_new[j,i] = self.smoke_concentration[j,i] + self.dt * (diff_x + diff_y)
        
        # Limiter les valeurs entre 0 et 1
        self.smoke_concentration = np.clip(smoke_new, 0, 1)
        
        # Assurer que les murs restent sans fumée
        self.smoke_concentration[self.wall_grid] = 0
        
        # Mise à jour de la température
        self.temperature *= 0.98  # Refroidissement légèrement plus lent

    def get_smoke_at_position(self, x, y):
        """Retourne la concentration de fumée à une position donnée"""
        if math.isnan(x) or math.isnan(y):
            return 0  # or some default value indicating invalid position

        grid_x = int(x / self.dx)
        grid_y = int(y / self.dy)
        if 0 <= grid_x < self.Nx and 0 <= grid_y < self.Ny:
            return self.smoke_concentration[grid_y, grid_x]
        return 0

    def get_temperature_at_position(self, x, y):
        """Retourne la température à une position donnée"""
        if math.isnan(x) or math.isnan(y):
            return 0  # or some default value indicating invalid position

        grid_x = int(x / self.dx)
        grid_y = int(y / self.dy)
        if 0 <= grid_x < self.Nx and 0 <= grid_y < self.Ny:
            return self.temperature[grid_y, grid_x]
        return 0

    def draw(self, screen):
        """Dessine la fumée et le feu"""
        # Surface pour la fumée avec transparence
        smoke_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        # Dessiner la fumée
        for i in range(self.Nx):
            for j in range(self.Ny):
                value = self.smoke_concentration[j,i]
                temp = self.temperature[j,i]
                if value > 0.01:  # Seuil minimum pour le rendu
                    color = self.get_smoke_color(value, temp)
                    pygame.draw.rect(smoke_surf, color,
                                   (i*self.dx, j*self.dy, self.dx+1, self.dy+1))
        
        screen.blit(smoke_surf, (0, 0))
        
        # Dessiner les sources de feu
        for fire_x, fire_y, strength, _ in self.fire_sources:
            x = int(fire_x * self.dx)
            y = int(fire_y * self.dy)
            size = int(8 * strength)
            pygame.draw.circle(screen, (255, 50, 0), (x, y), size)

    def get_smoke_color(self, smoke_value, temp_value):
        """Calcule la couleur de la fumée"""
        if smoke_value < 0.01:
            return (0, 0, 0, 0)
        
        smoke_value = min(0.95, smoke_value)
        base_gray = 30
        
        if temp_value < 0.3:
            intensity = base_gray + int(70 * smoke_value)
            red = green = blue = intensity
        else:
            red = min(200, base_gray + int(150 * temp_value))
            green = min(150, base_gray + int(80 * temp_value))
            blue = base_gray

        alpha = int(180 * (0.3 + 0.7 * smoke_value))
        
        return (max(20, min(200, red)),
                max(20, min(200, green)),
                max(20, min(200, blue)),
                max(50, min(200, alpha)))
