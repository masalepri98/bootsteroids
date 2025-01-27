import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT

# Base class for game objects
class CircleShape:
    containers = []  # Will be set from main.py
    
    def __init__(self, x: int, y: int, radius: int):
        self.position = pygame.Vector2(x, y)
        self.radius = radius
        self.velocity = pygame.Vector2(0, 0)
        
        # Add self to all containers
        for container in self.containers:
            container.append(self)

    def wrap_position(self):
        """Wrap position around screen edges"""
        # Wrap horizontally
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
            
        # Wrap vertically
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius

    def kill(self):
        """Removes this object from all its containers"""
        for container in self.containers:
            if self in container:
                container.remove(self)

    def collides_with(self, other: 'CircleShape') -> bool:
        """Returns True if this shape collides with another CircleShape"""
        # Get distance between centers
        distance = self.position.distance_to(other.position)
        # Collision occurs if distance is less than sum of radii
        return distance < (self.radius + other.radius)

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass