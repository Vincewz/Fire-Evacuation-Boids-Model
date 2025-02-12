import pygame
import random
import math
from config import *

class Boid:
    def __init__(self, x, y, game_map, room_id=1):
        self.position = pygame.Vector2(x, y)
        angle = random.uniform(0, 2 * math.pi)
        self.velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * MAX_SPEED
        self.last_direction = pygame.Vector2(self.velocity).normalize()
        self.map = game_map
        self.current_room = room_id
        self.queued_at_exit = None
        self.exit_pass = []

        #Percived risk
        self.boid_PR = 0
        
        # État de santé
        self.health = 100.0
        self.is_alive = True
        self.base_speed = MAX_SPEED
        
    def update_health(self, smoke_concentration, temperature):
        """Met à jour la santé du boid en fonction de la fumée"""
        if not self.is_alive:
            return
            
        # Dégâts basés sur la concentration de fumée et la température
        smoke_damage = smoke_concentration * SMOKE_DAMAGE_RATE
        heat_damage = temperature * HEAT_DAMAGE_RATE
        
        self.health -= (smoke_damage + heat_damage)
        
        # Vérification de la mort
        if self.health <= 0:
            self.is_alive = False
            self.health = 0
            
    def get_visible_boids(self, boids):
        """Vision réduite par la fumée"""
        if not self.is_alive:
            return []
            
        visible = []
        for boid in boids:
            if boid != self and boid.is_alive:
                distance = self.position.distance_to(boid.position)
                if distance < VISION_RADIUS:
                    visible.append(boid)
        return visible

    def align(self, visible_boids):
        """Alignement avec les autres boids"""
        if not visible_boids:
            return pygame.Vector2(0, 0)
        avg_velocity = pygame.Vector2(0, 0)
        for boid in visible_boids:
            avg_velocity += boid.velocity
        avg_velocity /= len(visible_boids)
        return avg_velocity - self.velocity
        
    def cohere(self, visible_boids):
        """Cohésion avec les autres boids"""
        if not visible_boids:
            return pygame.Vector2(0, 0)
        center_of_mass = pygame.Vector2(0, 0)
        for boid in visible_boids:
            center_of_mass += boid.position
        center_of_mass /= len(visible_boids)
        return center_of_mass - self.position
        
    def separate(self, visible_boids):
        """Séparation des autres boids"""
        if not visible_boids:
            return pygame.Vector2(0, 0)
        separation = pygame.Vector2(0, 0)
        for boid in visible_boids:
            diff = self.position - boid.position
            distance = diff.length()
            if distance < BOID_RADIUS * 4:
                if distance > 0:
                    separation += diff.normalize() / distance
        return separation

    def get_smoke_avoidance_force(self, fire_manager):
        """Calcule la force d'évitement de la fumée en tenant compte des murs"""
        avoidance = pygame.Vector2(0, 0)
        check_radius = SMOKE_AVOIDANCE_RADIUS
        check_points = 8  # Nombre de points à vérifier autour du boid
        
        # Vérifier si le boid est déjà dans la fumée
        current_smoke = fire_manager.get_smoke_at_position(self.position.x, self.position.y)
        if current_smoke > 0.1:
            return avoidance  # Pas de force d'évitement si déjà dans la fumée
        
        for i in range(check_points):
            angle = 2 * math.pi * i / check_points
            check_pos = self.position + pygame.Vector2(
                math.cos(angle) * check_radius,
                math.sin(angle) * check_radius
            )
            
            # Vérifier si un mur bloque la vue entre le boid et le point de vérification
            if self.map.is_line_of_sight_clear(self.position, check_pos):
                # Obtenir la concentration de fumée au point de vérification seulement si visible
                smoke = fire_manager.get_smoke_at_position(check_pos.x, check_pos.y)
                
                if smoke > 0.1:  # Seuil de détection de la fumée
                    # Vecteur d'évitement pointant à l'opposé de la fumée
                    avoid_vector = self.position - check_pos
                    if avoid_vector.length() > 0:
                        avoid_vector.normalize_ip()
                        # Force proportionnelle à la concentration de fumée
                        avoidance += avoid_vector * (smoke * SMOKE_AVOIDANCE_STRENGTH)
        
        return avoidance
    
    def update_boid_PR(self, fire_manager):
        if self.boid_PR == 1:  #Once at 1, don't make the check again
            return
    
        range_test = [SMOKE_AVOIDANCE_RADIUS * 1.5, SMOKE_AVOIDANCE_RADIUS, SMOKE_AVOIDANCE_RADIUS * 0.5]
        check_points = 8 
        slf_smoke = fire_manager.get_smoke_at_position(self.position.x, self.position.y)

        if slf_smoke > 0.1 : # try on the boids position
            self.boid_PR = 1
            return

        for range_test in range_test : 
            for i in range(check_points):
                angle = 2 * math.pi * i / check_points  
                check_pos = self.position + pygame.Vector2(
                    math.cos(angle) * range_test,
                    math.sin(angle) * range_test
                )
        
            # check for wall
                if self.map.is_line_of_sight_clear(self.position, check_pos):
                    smoke = fire_manager.get_smoke_at_position(check_pos.x, check_pos.y)
            
                    if smoke > 0.1:  
                     self.boid_PR = 1 
                     return  

    def find_nearest_exit(self):
        """Trouve la sortie la plus appropriée basée sur l'orientation du boid"""
        if self.current_room is None:
            return None
            
        current_room = ROOMS[self.current_room]
        best_exit = None
        best_score = float('-inf')
        
        # Normaliser le vecteur de vélocité du boid
        if self.velocity.length() > 0:
            boid_direction = self.velocity.normalize()
        else:
            return None
        
        for exit_info in current_room["exits"]:
            exit_pos = pygame.Vector2(exit_info["position"])
            
            # Vecteur vers la sortie
            to_exit = exit_pos - self.position
            distance = to_exit.length()
            if distance > 0:
                to_exit = to_exit.normalize()
                
                # Calculer l'alignement entre la direction du boid et la direction vers la sortie
                direction_alignment = boid_direction.dot(to_exit)
                
                # Le score favorise les sorties vers lesquelles le boid est orienté
                # et pénalise légèrement la distance
                score = direction_alignment * 2.0 - (distance / 1000.0)
                
                if score > best_score:
                    best_score = score
                    best_exit = exit_pos
                    
        return best_exit


    def check_exit_collision(self, exit_manager):
        """Vérifie les collisions avec les sorties"""
        if self.queued_at_exit or not self.is_alive:
            return
            
        current_room = ROOMS[self.current_room]
        for exit_info in current_room["exits"]:
            exit_pos = pygame.Vector2(exit_info["position"])
            # Augmenter légèrement la zone de détection
            detection_radius = exit_info["width"] * 0.75  # Zone de détection plus large
            
            if self.position.distance_to(exit_pos) < detection_radius:
                # Vérifier si le boid se dirige approximativement vers la sortie
                exit_direction = pygame.Vector2(exit_info["direction"])
                to_exit = (exit_pos - self.position).normalize()
                # Rendre la condition d'angle moins stricte
                angle_threshold = 0.3  # Plus permissif que 0.5
                
                if to_exit.dot(exit_direction) > -angle_threshold:  # Le boid est face à la sortie
                    # Essayer plusieurs fois d'ajouter le boid à la queue si nécessaire
                    max_attempts = 3
                    for _ in range(max_attempts):
                        if exit_manager.try_queue_boid(self, exit_info["id"]):
                            self.queued_at_exit = exit_info["id"]
                            # Ajuster la position du boid pour qu'il soit exactement à la sortie
                            self.position = exit_pos
                            self.velocity *= 0  # Arrêter le mouvement
                            return True
        return False
        
    def update(self, boids, exit_manager, fire_manager=None):
        """Mise à jour avec évitement de la fumée modifié"""
        if not self.is_alive or self.current_room is None or self.queued_at_exit:
            return
            
        # Mise à jour de la santé et des percived risk
        if fire_manager:
            smoke = fire_manager.get_smoke_at_position(self.position.x, self.position.y)
            temp = fire_manager.get_temperature_at_position(self.position.x, self.position.y)
            self.update_health(smoke, temp)
            self.update_boid_PR(fire_manager)

        is_stopped = False
        changed_direction = False

        #panic behaviour
        if self.boid_PR == 1:
            #stop
            if random.random() < CHANCE_TO_STOP:
                self.velocity *= 0
                is_stopped = True

            #random change of dierction
            elif random.random() < CHANCE_TO_CHANGE_DIRECTION:
                angle = random.uniform(0, 2 * math.pi)
                self.velocity = pygame.Vector2( math.cos(angle), math.sin(angle)) * random.uniform(0.5, self.base_speed)
                changed_direction = True
                
        if not is_stopped and not changed_direction:  
            # Forces de base
            visible_boids = [b for b in self.get_visible_boids(boids) 
                            if b.current_room == self.current_room]
            
            alignment = self.align(visible_boids)
            cohesion = self.cohere(visible_boids)
            separation = self.separate(visible_boids)
            wall_avoidance = self.map.get_wall_avoidance_force(self.position)
            
            # Force d'évitement de la fumée
            smoke_avoidance = pygame.Vector2(0, 0)
            if fire_manager:
                smoke_avoidance = self.get_smoke_avoidance_force(fire_manager)
            
            exit_attraction = pygame.Vector2(0, 0)#def of the attraction 

            # Force vers la sortie (plus forte en présence de fumée)
            if self.boid_PR == 1:
                nearest_exit = self.find_nearest_exit()
                exit_attraction = pygame.Vector2(0, 0)
                if nearest_exit:
                    to_exit = nearest_exit - self.position
                    if to_exit.length() > 0:
                        exit_attraction = to_exit.normalize() * EXIT_STRENGTH
                        # Augmenter l'attraction vers la sortie si il y a de la fumée
                        if fire_manager:
                            smoke = fire_manager.get_smoke_at_position(self.position.x, self.position.y)
                            exit_attraction *= (1 + smoke * 2)
            
            # Appliquer toutes les forces
            self.velocity += (
                alignment * ALIGNMENT_STRENGTH +
                cohesion * COHESION_STRENGTH +
                separation * SEPARATION_STRENGTH +
                wall_avoidance * WALL_AVOIDANCE_STRENGTH +
                smoke_avoidance +
                exit_attraction
            )
        
        # Limiter la vitesse
        current_speed = self.base_speed

        if self.boid_PR == 0:
            current_speed *= 0.5

        if fire_manager:
            # Ralentissement dans la fumée
            smoke = fire_manager.get_smoke_at_position(self.position.x, self.position.y)
            current_speed *= (1 - smoke * SMOKE_SLOWDOWN_FACTOR) 
            
        if not is_stopped and self.velocity.length() < 0.1:
            self.velocity = pygame.Vector2(self.last_direction) * (current_speed * 0.5)
        elif self.velocity.length() > current_speed:
            self.velocity.scale_to_length(current_speed)
        
        #if boid moov save last direction
        if self.velocity.length() > 0:  
            self.last_direction = self.velocity.normalize()
        
        # Mise à jour de la position
        new_position = self.position + self.velocity
        if not self.map.is_point_in_wall(new_position):
            self.position = new_position
            
        # Vérification des sorties
        self.check_exit_collision(exit_manager)

        

    

        
    def draw(self, screen):
        """Dessine le boid avec indication de santé"""
        if not self.is_alive or self.current_room is None:
            return
        
        indicator_color = (0, 255, 0) if self.boid_PR == 0 else (255, 0, 0)
        indicator_position = (self.position.x, self.position.y - BOID_RADIUS - 8)
        pygame.draw.circle(screen, indicator_color, indicator_position, 4)
            
        # Déterminer l'angle en fonction de la vélocité ou utiliser un angle par défaut
        if self.velocity.length() > 0:
            angle = math.atan2(self.velocity.y, self.velocity.x)
        else:
            angle = math.atan2(self.last_direction.y, self.last_direction.x)
        
        points = [
            (self.position.x + BOID_RADIUS * math.cos(angle),
            self.position.y + BOID_RADIUS * math.sin(angle)),
            (self.position.x + BOID_RADIUS * math.cos(angle + 2.6),
            self.position.y + BOID_RADIUS * math.sin(angle + 2.6)),
            (self.position.x + BOID_RADIUS * math.cos(angle - 2.6),
            self.position.y + BOID_RADIUS * math.sin(angle - 2.6))
        ]
        
        # Déterminer la couleur
        if self.queued_at_exit:
            color = (200, 100, 100)
        else:
            health_ratio = self.health / 100.0
            red = int(255 * (1 - health_ratio))
            green = int(255 * health_ratio)
            blue = 50
            color = (red, green, blue)
        
        pygame.draw.polygon(screen, color, points)
        
        # Barre de vie
        health_width = 20
        health_height = 3
        health_x = self.position.x - health_width/2
        health_y = self.position.y - BOID_RADIUS - 5
        
        # Fond rouge (santé manquante)
        pygame.draw.rect(screen, (255, 0, 0),
                        (health_x, health_y, health_width, health_height))
        # Barre verte (santé restante)
        pygame.draw.rect(screen, (0, 255, 0),
                        (health_x, health_y, health_width * (self.health/100), health_height))
            
