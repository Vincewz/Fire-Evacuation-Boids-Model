import pygame
import numpy as np

class FireSmokeSimulation:
    def __init__(self, width=1200, height=800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Simulation de Fumée d'Incendie avec Murs - Vue du Dessus")
        
        # Paramètres de la simulation
        self.Nx = 240
        self.Ny = 160
        self.dx = width / self.Nx
        self.dy = height / self.Ny
        self.dt = 1.35
        self.D = 3.8
        
        # Grilles
        self.C = np.zeros((self.Ny, self.Nx))  # Concentration de fumée
        self.T = np.zeros((self.Ny, self.Nx))  # Température
        self.vx = np.zeros((self.Ny, self.Nx))
        self.vy = np.zeros((self.Ny, self.Nx))
        self.walls = np.zeros((self.Ny, self.Nx), dtype=bool)  # Grille des murs
        
        # Source de l'incendie
        self.fire_x = int(self.Nx * 0.3)
        self.fire_y = int(self.Ny * 0.5)
        self.fire_strength = 2.0
        
        # Direction du vent
        self.wind_angle = np.pi * 0.25  # 45 degrés par défaut
        self.wind_speed = 0.5
        
        # États
        self.paused = False
        self.show_vectors = True
        self.drawing_wall = False
        
        self.setup_wind_field()
        self.setup_walls()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

    def setup_walls(self):
        """Configure les murs initiaux de la pièce"""
        wall_thickness = 3
        
        # Murs extérieurs
        self.walls[:, :wall_thickness] = True  # Mur gauche
        self.walls[:, -wall_thickness:] = True  # Mur droit
        self.walls[:wall_thickness, :] = True  # Mur haut
        self.walls[-wall_thickness:, :] = True  # Mur bas
        
        # Porte (ouverture dans le mur droit)
        door_height = 40
        door_start = self.Ny // 2 - door_height // 2
        self.walls[door_start:door_start + door_height, -wall_thickness:] = False
        
    def setup_wind_field(self):
        """Configure le champ de vent de base"""
        self.vx = np.ones((self.Ny, self.Nx)) * self.wind_speed * np.cos(self.wind_angle)
        self.vy = np.ones((self.Ny, self.Nx)) * self.wind_speed * np.sin(self.wind_angle)
        
        self.vx += np.random.randn(self.Ny, self.Nx) * 0.4
        self.vy += np.random.randn(self.Ny, self.Nx) * 0.4
        
        # Mettre à zéro le vent dans les murs
        self.vx[self.walls] = 0
        self.vy[self.walls] = 0

    def add_fire_smoke(self):
        """Ajoute de la fumée à la source de l'incendie"""
        radius = 5
        for i in range(self.fire_x-radius, self.fire_x+radius+1):
            for j in range(self.fire_y-radius, self.fire_y+radius+1):
                if (0 <= i < self.Nx and 0 <= j < self.Ny and 
                    not self.walls[j,i]):  # Vérifie qu'il n'y a pas de mur
                    dist = np.sqrt((i-self.fire_x)**2 + (j-self.fire_y)**2)
                    if dist < radius:
                        self.C[j,i] = min(1.0, self.C[j,i] + 
                                        self.fire_strength * (1 - dist/radius))
                        self.T[j,i] = self.fire_strength

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_v:
                    self.show_vectors = not self.show_vectors
                elif event.key == pygame.K_c:
                    self.C = np.zeros((self.Ny, self.Nx))
                    self.T = np.zeros((self.Ny, self.Nx))
                elif event.key == pygame.K_w:  # Effacer tous les murs
                    self.walls.fill(False)
                    self.setup_walls()
                elif event.key == pygame.K_UP:
                    self.wind_speed = min(5.0, self.wind_speed * 1.2)
                    self.setup_wind_field()
                elif event.key == pygame.K_DOWN:
                    self.wind_speed = max(0.5, self.wind_speed / 1.2)
                    self.setup_wind_field()
                elif event.key == pygame.K_LEFT:
                    self.wind_angle = (self.wind_angle + 0.1) % (2 * np.pi)
                    self.setup_wind_field()
                elif event.key == pygame.K_RIGHT:
                    self.wind_angle = (self.wind_angle - 0.1) % (2 * np.pi)
                    self.setup_wind_field()
                elif event.key == pygame.K_f:
                    self.fire_strength = min(2.0, self.fire_strength * 1.2)
                elif event.key == pygame.K_d:
                    self.fire_strength = max(0.2, self.fire_strength / 1.2)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:  # Shift maintenu
                        self.drawing_wall = True
                    else:  # Déplacer le feu
                        x, y = pygame.mouse.get_pos()
                        grid_x, grid_y = int(x / self.dx), int(y / self.dy)
                        if not self.walls[grid_y, grid_x]:
                            self.fire_x = grid_x
                            self.fire_y = grid_y
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Clic gauche relâché
                    self.drawing_wall = False
            elif event.type == pygame.MOUSEMOTION:
                if self.drawing_wall:  # Dessiner des murs en maintenant Shift + clic gauche
                    x, y = pygame.mouse.get_pos()
                    grid_x, grid_y = int(x / self.dx), int(y / self.dy)
                    if 0 <= grid_x < self.Nx and 0 <= grid_y < self.Ny:
                        self.walls[grid_y, grid_x] = True
                        self.C[grid_y, grid_x] = 0  # Effacer la fumée dans le mur
        return True

    def update(self):
        if self.paused:
            return
                
        self.add_fire_smoke()
        
        C_new = np.copy(self.C)
        for i in range(1, self.Nx-1):
            for j in range(1, self.Ny-1):
                # Si c'est un mur mais pas la position du feu, on met à zéro
                if self.walls[j,i] and not (i == self.fire_x and j == self.fire_y):
                    C_new[j,i] = 0
                    continue
                
                # Vérifie les murs voisins
                left_wall = self.walls[j,i-1]
                right_wall = self.walls[j,i+1]
                up_wall = self.walls[j-1,i]
                down_wall = self.walls[j+1,i]
                
                # Advection avec le vent
                adv_x = 0
                if not left_wall and self.vx[j,i] > 0:
                    adv_x = self.vx[j,i] * (self.C[j,i] - self.C[j,i-1])/self.dx
                elif not right_wall and self.vx[j,i] < 0:
                    adv_x = self.vx[j,i] * (self.C[j,i+1] - self.C[j,i])/self.dx
                
                adv_y = 0
                if not up_wall and self.vy[j,i] > 0:
                    adv_y = self.vy[j,i] * (self.C[j,i] - self.C[j-1,i])/self.dy
                elif not down_wall and self.vy[j,i] < 0:
                    adv_y = self.vy[j,i] * (self.C[j+1,i] - self.C[j,i])/self.dy
                
                # Diffusion (seulement dans les directions sans mur)
                diff_x = diff_y = 0
                if not left_wall and not right_wall:
                    diff_x = self.D * (self.C[j,i+1] - 2*self.C[j,i] + self.C[j,i-1])/self.dx**2
                if not up_wall and not down_wall:
                    diff_y = self.D * (self.C[j+1,i] - 2*self.C[j,i] + self.C[j-1,i])/self.dy**2
                
                # Mise à jour de la concentration
                C_new[j,i] = self.C[j,i] - self.dt * (adv_x + adv_y) + self.dt * (diff_x + diff_y)
        
        # Assurer que les murs (sauf position du feu) restent à zéro
        wall_mask = self.walls & ~((np.arange(self.Nx) == self.fire_x)[:, None] & 
                                (np.arange(self.Ny) == self.fire_y)[None, :]).T
        C_new[wall_mask] = 0
        
        # Limiter les valeurs entre 0 et 1
        self.C = np.clip(C_new, 0, 1)
        
        # Mise à jour du champ de vent avec turbulence
        self.vx += np.random.randn(self.Ny, self.Nx) * 0.1
        self.vy += np.random.randn(self.Ny, self.Nx) * 0.1
        
        # Maintenir la direction principale du vent (sauf dans les murs)
        mask = ~self.walls
        self.vx[mask] = 0.9 * self.vx[mask] + 0.1 * (self.wind_speed * np.cos(self.wind_angle))
        self.vy[mask] = 0.9 * self.vy[mask] + 0.1 * (self.wind_speed * np.sin(self.wind_angle))
        
        # Garantir que le vent est nul dans les murs (sauf position du feu)
        self.vx[wall_mask] = 0
        self.vy[wall_mask] = 0

    def get_smoke_color(self, smoke_value, temp_value):
        """Retourne la couleur de la fumée en fonction de sa densité et de la température"""
        if smoke_value < 0.01:  # Augmenter légèrement le seuil minimal
            return (0, 0, 0, 0)
        
        # Lissage de la valeur de fumée pour éviter les changements brusques
        smoke_value = min(0.95, smoke_value)  # Limite supérieure pour éviter le blanc pur
        
        # Base plus sombre pour la fumée
        base_gray = 30  # Réduit de 50 à 30 pour une fumée plus sombre
        
        # Calcul des composantes RGB avec transitions plus douces
        if temp_value < 0.3:
            # Fumée froide : rester dans les tons gris sombres
            intensity = base_gray + int(70 * smoke_value)  # Réduit la plage de variation
            red = green = blue = intensity
        else:
            # Fumée chaude : teintes rouge/orange avec transitions plus douces
            red = min(200, base_gray + int(150 * temp_value))  # Réduit le maximum
            green = min(150, base_gray + int(80 * temp_value))  # Réduit le maximum
            blue = base_gray

        # Ajustement de l'opacité avec une variation plus progressive
        alpha = int(180 * (0.3 + 0.7 * smoke_value))  # Opacité minimum de 30%
        
        # Assurer que toutes les valeurs sont dans la plage valide
        red = max(20, min(200, red))    # Évite le noir et blanc purs
        green = max(20, min(200, green))
        blue = max(20, min(200, blue))
        alpha = max(50, min(200, alpha))  # Maintient une opacité minimum

        return (red, green, blue, alpha)

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        # Dessiner la fumée
        smoke_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for i in range(self.Nx):
            for j in range(self.Ny):
                value = self.C[j,i]
                temp = self.T[j,i]
                if value > 0.01:
                    color = self.get_smoke_color(value, temp)
                    pygame.draw.rect(smoke_surf, color,
                                   (i*self.dx, j*self.dy, self.dx+1, self.dy+1))
        
        self.screen.blit(smoke_surf, (0, 0))
        
        # Dessiner les murs
        for i in range(self.Nx):
            for j in range(self.Ny):
                if self.walls[j,i]:
                    pygame.draw.rect(self.screen, (100, 100, 100),
                                   (i*self.dx, j*self.dy, self.dx+1, self.dy+1))
        
        # Dessiner le foyer de l'incendie
        pygame.draw.circle(self.screen, (255, 50, 0),
                         (int(self.fire_x * self.dx), int(self.fire_y * self.dy)), 8)
        
        # Dessiner les vecteurs de vent
        if self.show_vectors:
            for i in range(0, self.Nx, 15):
                for j in range(0, self.Ny, 15):
                    if not self.walls[j,i]:
                        x = int(i * self.dx)
                        y = int(j * self.dy)
                        vx = self.vx[j,i] * 15
                        vy = self.vy[j,i] * 15
                        if abs(vx) > 0.1 or abs(vy) > 0.1:
                            pygame.draw.line(self.screen, (150, 150, 150),
                                           (x, y), (x + vx, y + vy), 1)
        
        
        # Afficher les informations
        texts = [
            "Clic: Move fire",
            "Shift+Clic: Draw wall",
            f"Vent: {self.wind_speed:.1f}",
            f"Angle: {int(np.degrees(self.wind_angle))}°",
            "↑↓: Wind speed",
            "←→: Wind direction",
            "F/D: Fire strength",
            "V: Vectors",
            "C: clean smoke",
            "W: clean wall"
        ]
        
        for i, text in enumerate(texts):
            text_surface = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (20, 20 + i*30))
        
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    sim = FireSmokeSimulation()
    sim.run()