import pygame
from collections import deque
import time
from config import *

class ExitQueue:
    def __init__(self, exit_info):
        self.exit_info = exit_info
        self.queue = deque()
        self.processing = {}  # {boid_id: start_time}
        self.last_process_time = time.time()
        
    def can_add(self):
        return len(self.queue) < EXIT_QUEUE_MAX_SIZE
        
    def add_boid(self, boid):
        if self.can_add():
            self.queue.append(boid)
            return True
        return False
        
    def start_processing(self, boid):
        self.processing[id(boid)] = time.time()
        
    def update(self):
        current_time = time.time()
        processed_boids = []
        
        # Process waiting boids
        if self.queue and len(self.processing) < self.exit_info["flow_rate"]:
            wait_time = 1.0 / self.exit_info["flow_rate"]
            if current_time - self.last_process_time >= wait_time:
                boid = self.queue.popleft()
                self.start_processing(boid)
                self.last_process_time = current_time
        
        # Check for completed processing
        for boid_id, start_time in list(self.processing.items()):
            process_time = EXIT_PROCESSING_TIME[self.exit_info["id"]] / 1000.0  # Convert to seconds
            if current_time - start_time >= process_time:
                processed_boids.append((boid_id, self.exit_info))
                del self.processing[boid_id]
                        
        return processed_boids

class ExitManager:
    def __init__(self, rooms):
        self.rooms = rooms
        self.exit_queues = {}
        self.initialize_queues()
        
    def initialize_queues(self):
        for room_id, room in self.rooms.items():
            for exit_info in room["exits"]:
                self.exit_queues[exit_info["id"]] = ExitQueue(exit_info)
                
    def get_exit_info(self, exit_id):
        for room in self.rooms.values():
            for exit_info in room["exits"]:
                if exit_info["id"] == exit_id:
                    return exit_info
        return None

    def update_boid_room(self, boid, exit_info):
        if exit_info:
            if exit_info["to_room"] is None:  # C'est une sortie finale
                boid.current_room = None  # Marque le boid comme sorti
                boid.queued_at_exit = None
                return True
            elif exit_info["spawn_point"]:
                # Téléporter le boid au point d'apparition de la nouvelle salle
                boid.position = pygame.Vector2(exit_info["spawn_point"])
                boid.current_room = exit_info["to_room"]
                # Réinitialiser la vitesse dans la direction de la sortie
                direction = pygame.Vector2(exit_info["direction"])
                boid.velocity = direction * MAX_SPEED
                boid.queued_at_exit = None
                return True
        return False
        
    def try_queue_boid(self, boid, exit_id):
        if exit_id in self.exit_queues:
            return self.exit_queues[exit_id].add_boid(boid)
        return False
        
    def update(self, boids):
        for exit_id, queue in self.exit_queues.items():
            processed = queue.update()
            for boid_id, exit_info in processed:
                # Find the corresponding boid
                for boid in boids:
                    if id(boid) == boid_id:
                        self.update_boid_room(boid, exit_info)
                        break

    def draw_queues(self, screen):
        for exit_id, queue in self.exit_queues.items():
            if queue.queue or queue.processing:
                exit_info = self.get_exit_info(exit_id)
                pos = exit_info["position"]
                # Draw exit area
                pygame.draw.circle(screen, EXIT_COLOR, pos, exit_info["width"]//2, 2)
                # Draw queue count
                font = pygame.font.Font(None, 24)
                count = len(queue.queue) + len(queue.processing)
                text = font.render(str(count), True, (255, 255, 255))
                screen.blit(text, (pos[0] - 5, pos[1] - 20))