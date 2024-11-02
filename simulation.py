import pygame
from config import *
import random
from boid import Boid
from map_utils import Map

class Simulation:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sequential Exits Boids Simulation")
        self.map = Map()
        self.boids = self.create_boids()
        
    def create_boids(self):
        boids = []
        room = [110, 110, 380, 380]  # Définir la zone de spawn des boids
        for _ in range(NUM_BOIDS):
            x = random.randint(room[0], room[0] + room[2])
            y = random.randint(room[1], room[1] + room[3])
            boids.append(Boid(x, y, self.map))
        return boids

    def run(self):
        running = True
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Clear screen
            self.screen.fill(BACKGROUND_COLOR)
            
            # Draw map
            self.map.draw(self.screen)
            
            # Update and draw boids
            for boid in self.boids:
                boid.update(self.boids)
                boid.draw(self.screen)

            # Draw simulation info
            font = pygame.font.Font(None, 36)
            text = font.render(f"Boids: {len(self.boids)}", True, (255, 255, 255))
            self.screen.blit(text, (10, 10))
            
            # Refresh screen
            pygame.display.flip()
            clock.tick(60)
            
        pygame.quit()