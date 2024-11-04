import pygame
import random
import math
from config import *

class Boid:
    def __init__(self, x, y, game_map, room_id=1):
        self.position = pygame.Vector2(x, y)
        angle = random.uniform(0, 2 * math.pi)
        self.velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * MAX_SPEED
        self.map = game_map
        self.current_room = room_id
        self.queued_at_exit = None
        self.exit_pass = []
        
    def get_visible_boids(self, boids):
        visible = []
        for boid in boids:
            if boid != self:
                distance = self.position.distance_to(boid.position)
                if distance < VISION_RADIUS:
                    visible.append(boid)
        return visible
        
    def check_exit_collision(self, exit_manager):
        if self.queued_at_exit:
            return
            
        current_room = ROOMS[self.current_room]
        for exit_info in current_room["exits"]:
            exit_pos = pygame.Vector2(exit_info["position"])
            # Check if within exit radius (using exit width)
            if self.position.distance_to(exit_pos) < exit_info["width"] / 2:
                # Check if moving towards exit
                exit_direction = pygame.Vector2(exit_info["direction"])
                if self.velocity.normalize().dot(exit_direction) > 0.5:
                    if exit_manager.try_queue_boid(self, exit_info["id"]):
                        self.queued_at_exit = exit_info["id"]
                        break
    
    def update(self, boids, exit_manager):
        # Si le boid est sorti ou en file d'attente, ne pas mettre à jour
        if self.current_room is None or self.queued_at_exit:
            return

        # Filter visible boids from same room
        visible_boids = [b for b in self.get_visible_boids(boids) 
                        if b.current_room == self.current_room]
        
        # Calculate forces
        alignment = self.align(visible_boids)
        cohesion = self.cohere(visible_boids)
        separation = self.separate(visible_boids)
        wall_avoidance = self.map.get_wall_avoidance_force(self.position)
        
        # Find nearest exit in current room
        current_room = ROOMS[self.current_room]
        nearest_exit = None
        min_distance = float('inf')
        
        for exit_info in current_room["exits"]:
            exit_pos = pygame.Vector2(exit_info["position"])
            dist = self.position.distance_to(exit_pos)
            if dist < min_distance:
                min_distance = dist
                nearest_exit = exit_pos
        
        # Calculate exit attraction
        exit_attraction = pygame.Vector2(0, 0)
        if nearest_exit:
            to_exit = nearest_exit - self.position
            distance = to_exit.length()
            if distance > 0:
                # Force inversement proportionnelle à la distance
                exit_attraction = to_exit.normalize() * EXIT_STRENGTH * (1 + VISION_RADIUS/max(distance, 1))
        
        # Apply all forces
        self.velocity += (alignment * ALIGNMENT_STRENGTH +
                        cohesion * COHESION_STRENGTH +
                        separation * SEPARATION_STRENGTH +
                        wall_avoidance * WALL_AVOIDANCE_STRENGTH +
                        exit_attraction)
        
        # Limit speed
        if self.velocity.length() > MAX_SPEED:
            self.velocity.scale_to_length(MAX_SPEED)
        
        # Update position if not in wall
        new_position = self.position + self.velocity
        if not self.map.is_point_in_wall(new_position):
            self.position = new_position
            
        # Check exit collisions
        self.check_exit_collision(exit_manager)
        
    def align(self, visible_boids):
        if not visible_boids:
            return pygame.Vector2(0, 0)
        avg_velocity = pygame.Vector2(0, 0)
        for boid in visible_boids:
            avg_velocity += boid.velocity
        avg_velocity /= len(visible_boids)
        return avg_velocity - self.velocity
        
    def cohere(self, visible_boids):
        if not visible_boids:
            return pygame.Vector2(0, 0)
        center_of_mass = pygame.Vector2(0, 0)
        for boid in visible_boids:
            center_of_mass += boid.position
        center_of_mass /= len(visible_boids)
        return center_of_mass - self.position
        
    def separate(self, visible_boids):
        if not visible_boids:
            return pygame.Vector2(0, 0)
        separation = pygame.Vector2(0, 0)
        for boid in visible_boids:
            diff = self.position - boid.position
            distance = diff.length()
            if distance < BOID_RADIUS * 4:  # Separation radius
                if distance > 0:  # Avoid division by zero
                    separation += diff.normalize() / distance
        return separation
        
    def draw(self, screen):
        # Ne pas dessiner les boids sortis
        if self.current_room is None:
            return
            
        # Calculate angle for triangle
        if self.velocity.length() > 0:
            angle = math.atan2(self.velocity.y, self.velocity.x)
            points = [
                (self.position.x + BOID_RADIUS * math.cos(angle),
                self.position.y + BOID_RADIUS * math.sin(angle)),
                (self.position.x + BOID_RADIUS * math.cos(angle + 2.6),
                self.position.y + BOID_RADIUS * math.sin(angle + 2.6)),
                (self.position.x + BOID_RADIUS * math.cos(angle - 2.6),
                self.position.y + BOID_RADIUS * math.sin(angle - 2.6))
            ]
            
            # Different color if queued at exit
            color = (200, 100, 100) if self.queued_at_exit else BOID_COLOR
            pygame.draw.polygon(screen, color, points)