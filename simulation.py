# simulation.py
import pygame
import cv2
import numpy as np
from config import *
from boid import Boid
from map_utils import Map
import random

class SimulationRecorder:
    def __init__(self, record_fps=30):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sequential Exits Boids Simulation")
        self.map = Map()
        self.boids = self.create_boids()
        
        # Video recording setup
        self.is_recording = False
        self.video_writer = None
        self.record_fps = record_fps
        
    def create_boids(self):
        boids = []
        room = [110, 110, 380, 380]
        for _ in range(NUM_BOIDS):
            x = random.randint(room[0], room[0] + room[2])
            y = random.randint(room[1], room[1] + room[3])
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
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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

                if self.is_recording:
                    recording_text = font.render("Recording...", True, (255, 0, 0))
                    self.screen.blit(recording_text, (10, 50))
                    
                    if max_frames:
                        progress = f"Frame: {frame_count}/{max_frames}"
                        progress_text = font.render(progress, True, (255, 0, 0))
                        self.screen.blit(progress_text, (10, 90))
                
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