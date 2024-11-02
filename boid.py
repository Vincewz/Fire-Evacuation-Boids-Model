import pygame
import random
import math
from config import *

class Boid:
    def __init__(self, x, y, game_map):
        self.position = pygame.Vector2(x, y)
        angle = random.uniform(0, 2 * math.pi)
        self.velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * MAX_SPEED
        self.map = game_map
        self.exit_pass = []
        self.current_target = None
        self.current_target_id = None

    def update(self, boids):
        # Get next exit point and its ID
        next_exit, next_exit_id = self.map.get_nearest_exit_point(self.position, self.exit_pass)
        
        if next_exit:
            # Update current target if it's new
            if next_exit_id != self.current_target_id:
                self.current_target = next_exit
                self.current_target_id = next_exit_id
            
            # Calculate all forces
            alignment = self.align(boids)
            cohesion = self.cohere(boids)
            separation = self.separate(boids)
            attraction = self.attract_to_point(self.current_target)
            wall_avoidance = self.map.get_wall_avoidance_force(self.position)

            # Check if boid has reached current exit
            distance_to_exit = self.position.distance_to(self.current_target)
            if distance_to_exit < EXIT_PASS_DISTANCE and self.current_target_id not in self.exit_pass:
                self.exit_pass.append(self.current_target_id)
                self.current_target = None
                self.current_target_id = None

            # Apply forces
            self.velocity += (alignment * ALIGNMENT_STRENGTH +
                            cohesion * COHESION_STRENGTH +
                            separation * SEPARATION_STRENGTH +
                            attraction * EXIT_STRENGTH +
                            wall_avoidance * WALL_AVOIDANCE_STRENGTH)

            # Limit speed
            if self.velocity.length() > MAX_SPEED:
                self.velocity.scale_to_length(MAX_SPEED)

            # Update position if not in wall
            new_position = self.position + self.velocity
            if not self.map.is_point_in_wall((new_position.x, new_position.y)):
                self.position = new_position

    def align(self, boids):
        avg_velocity = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < VISION_RADIUS:
                avg_velocity += boid.velocity
                total += 1
        if total > 0:
            avg_velocity /= total
            avg_velocity = avg_velocity - self.velocity
        return avg_velocity

    def cohere(self, boids):
        center_of_mass = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            if boid != self and self.position.distance_to(boid.position) < VISION_RADIUS:
                center_of_mass += boid.position
                total += 1
        if total > 0:
            center_of_mass /= total
            return (center_of_mass - self.position)
        return pygame.Vector2(0, 0)

    def separate(self, boids):
        avoidance = pygame.Vector2(0, 0)
        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if boid != self and distance < BOID_RADIUS * 2:
                diff = self.position - boid.position
                if distance > 0:
                    diff /= distance
                avoidance += diff
        return avoidance

    def attract_to_point(self, target):
        if isinstance(target, pygame.Vector2):
            direction = target - self.position
            if direction.length() > 0:
                direction.normalize_ip()
            return direction
        return pygame.Vector2(0, 0)

    def draw(self, screen):
        # Draw boid as triangle
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
            pygame.draw.polygon(screen, BOID_COLOR, points)
            
            # Draw debug info - exit points passed
            font = pygame.font.Font(None, 20)
            text = font.render(f"Exits: {self.exit_pass}", True, (255, 255, 255))
            screen.blit(text, (self.position.x + 10, self.position.y + 10))