import pygame
import cv2
import numpy as np
from config import *
from boid import Boid
from map_utils import Map
from exit_manager import ExitManager
from fire_manager import FireManager
import random

class SimulationRecorder:
    def __init__(self, record_fps=30):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Fire Evacuation Simulation")
        self.map = Map()
        self.exit_manager = ExitManager(ROOMS)
        self.fire_manager = FireManager(ROOMS)
        self.boids = self.create_boids()
        # Video recording setup
        self.is_recording = False
        self.video_writer = None
        self.record_fps = record_fps
        
        # Statistics
        self.escaped_boids = 0
        self.dead_boids = 0
        self.simulation_time = 0
        
        # Clock and display
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.paused = False

    def create_boids(self):
        boids = []
        boids_per_room = NUM_BOIDS // len(ROOMS)
        remaining_boids = NUM_BOIDS % len(ROOMS)

        for room_id, room in ROOMS.items():
            num_room_boids = boids_per_room
            if remaining_boids > 0:
                num_room_boids += 1
                remaining_boids -= 1

            spawn = room["spawn_area"]
            for _ in range(num_room_boids):
                x = random.randint(spawn[0], spawn[0] + spawn[2])
                y = random.randint(spawn[1], spawn[1] + spawn[3])
                boids.append(Boid(x, y, self.map, room_id))

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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    if not self.is_recording:
                        self.start_recording()
                    else:
                        self.stop_recording()
        return True

    def update(self):
        if not self.paused:
            self.simulation_time += 1/60
            
            # Update fire and smoke
            self.fire_manager.update()

            # Update exit manager
            self.exit_manager.update(self.boids)
            
            # Remove escaped and dead boids
            self.remove_escaped_boids()
            
            # Update remaining boids
            for boid in self.boids:
                boid.update(self.boids, self.exit_manager, self.fire_manager)

    def remove_escaped_boids(self):
        active_boids = []
        for boid in self.boids:
            if not boid.is_alive:
                if boid in active_boids:
                    active_boids.remove(boid)
                if self.dead_boids < NUM_BOIDS:
                    self.dead_boids += 1
            elif boid.current_room is not None:
                active_boids.append(boid)
            else:
                if self.escaped_boids < NUM_BOIDS:
                    self.escaped_boids += 1
        self.boids = active_boids

    def draw_statistics(self):
        alive_boids = len([b for b in self.boids if b.is_alive])
        total_boids = NUM_BOIDS
        
        stats = [
            f"Time: {self.simulation_time:.1f}s",
            f"Active Boids: {alive_boids}",
            f"Escaped Boids: {self.escaped_boids}",
            f"Dead Boids: {self.dead_boids}",
            f"Survival Rate: {((alive_boids + self.escaped_boids) / total_boids * 100):.1f}%",
            f"Active Fires: {len(self.fire_manager.fire_sources)}"
        ]
        
        # Display statistics
        for i, text in enumerate(stats):
            surface = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(surface, (10, 10 + i * 30))
        
        # Controls
        controls = [
            "Space: Pause",
            "ESC: Quit",
            "R: Toggle Recording"
        ]
        
        for i, text in enumerate(controls):
            surface = self.font.render(text, True, (200, 200, 200))
            self.screen.blit(surface, (WIDTH - 200, 10 + i * 30))
        
        if self.is_recording:
            text = self.font.render("Recording...", True, (255, 0, 0))
            self.screen.blit(text, (WIDTH - 200, HEIGHT - 40))
        
        if self.paused:
            text = self.font.render("PAUSED", True, (255, 200, 0))
            self.screen.blit(text, (WIDTH//2 - 50, 10))

    def draw(self):
        # Clear screen
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw map
        self.map.draw(self.screen)
        
        # Draw fire and smoke
        self.fire_manager.draw(self.screen)
        
        # Draw exit queues
        self.exit_manager.draw_queues(self.screen)
        
        # Draw boids
        for boid in self.boids:
            boid.draw(self.screen)
        
        # Draw statistics
        self.draw_statistics()
        
        # Update display
        pygame.display.flip()
        
        # Capture frame if recording
        if self.is_recording:
            self.capture_frame()

    def run(self, max_frames=None):
        running = True
        frame_count = 0
        
        try:
            while running:
                if max_frames and frame_count >= max_frames:
                    break
                
                running = self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(60)
                frame_count += 1
                
        finally:
            if self.is_recording:
                self.stop_recording()
            pygame.quit()



if __name__ == "__main__":
    sim = SimulationRecorder()
    sim.run()