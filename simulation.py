import pygame
import cv2
import numpy as np
from config import *
from boid import Boid
from map_utils import Map
from exit_manager import ExitManager
import random

class SimulationRecorder:
    def __init__(self, record_fps=30):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Multi-Room Boids Simulation")
        self.map = Map()
        self.exit_manager = ExitManager(ROOMS)
        self.boids = self.create_boids()
        
        # Video recording setup
        self.is_recording = False
        self.video_writer = None
        self.record_fps = record_fps
        
        # Statistics
        self.escaped_boids = 0
        
    def create_boids(self):
        boids = []
        # Get spawn area for first room
        spawn = ROOMS[1]["spawn_area"]
        for _ in range(NUM_BOIDS):
            x = random.randint(spawn[0], spawn[0] + spawn[2])
            y = random.randint(spawn[1], spawn[1] + spawn[3])
            boids.append(Boid(x, y, self.map))
        return boids

    def start_recording(self, filename='simulation_recording.mp4'):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(filename, fourcc, self.record_fps, (WIDTH, HEIGHT))
        self.is_recording = True
        print(f"Started recording to {filename}")

    def stop_recording(self):
        if self.is_recording:
            self.video_writer.release()
            self.is_recording = False
            print("Recording stopped")

    def capture_frame(self):
        pixel_array = pygame.surfarray.array3d(self.screen)
        pixel_array = pixel_array.swapaxes(0, 1)
        frame = cv2.cvtColor(pixel_array, cv2.COLOR_RGB2BGR)
        self.video_writer.write(frame)

    def draw_statistics(self):
        font = pygame.font.Font(None, 36)
        stats = [
            f"Active Boids: {len(self.boids)}",
            f"Escaped Boids: {self.escaped_boids}",
        ]
        
        for i, text in enumerate(stats):
            surface = font.render(text, True, (255, 255, 255))
            self.screen.blit(surface, (10, 10 + i * 40))
            
        if self.is_recording:
            recording_text = font.render("Recording...", True, (255, 0, 0))
            self.screen.blit(recording_text, (10, 90))

    def remove_escaped_boids(self):
        # Remove boids that have reached the final exit
        active_boids = []
        for boid in self.boids:
            if boid.current_room is not None:  # None indicates the boid has escaped
                active_boids.append(boid)
            else:
                self.escaped_boids += 1
        self.boids = active_boids

    def run(self, max_frames=None):
        running = True
        clock = pygame.time.Clock()
        frame_count = 0
        
        try:
            while running:
                if max_frames and frame_count >= max_frames:
                    break
                    
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                        elif event.key == pygame.K_r:  # Toggle recording
                            if not self.is_recording:
                                self.start_recording()
                            else:
                                self.stop_recording()

                # Clear screen
                self.screen.fill(BACKGROUND_COLOR)
                
                # Update exit manager
                self.exit_manager.update(self.boids)
                
                # Remove escaped boids BEFORE updating remaining boids
                self.remove_escaped_boids()
                
                # Update and draw map
                self.map.draw(self.screen)
                
                # Draw exit queues
                self.exit_manager.draw_queues(self.screen)
                
                # Update and draw remaining boids
                for boid in self.boids:
                    boid.update(self.boids, self.exit_manager)
                    boid.draw(self.screen)
                
                # Draw statistics
                self.draw_statistics()
                
                # Capture frame if recording
                if self.is_recording:
                    self.capture_frame()
                
                # Refresh screen
                pygame.display.flip()
                clock.tick(self.record_fps)
                frame_count += 1
                
        finally:
            if self.is_recording:
                self.stop_recording()
            pygame.quit()

if __name__ == "__main__":
    simulation = SimulationRecorder()
    simulation.run()