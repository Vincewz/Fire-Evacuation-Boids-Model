class DirectionIndicator:
    def __init__(self, target_position, influence_radius):
        self.target_position = target_position
        self.influence_radius = influence_radius

    def is_within_influence(self, boid_position):
        dx = boid_position[0] - self.target_position[0]
        dy = boid_position[1] - self.target_position[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5
        return distance <= self.influence_radius

    def apply_influence(self, boid):
        if self.is_within_influence((boid.x, boid.y)):
            boid.target_position = self.target_position
