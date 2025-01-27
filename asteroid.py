import pygame
import random
import math
from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS, SCORE_LARGE, SCORE_MEDIUM, SCORE_SMALL
from explosion import Explosion

class Asteroid(CircleShape):
    # Static containers will be set from main.py
    containers = []
    
    def __init__(self, x: int, y: int, radius: int):
        super().__init__(x, y, radius)
        # Create lumpy shape
        self.vertices = []
        num_vertices = random.randint(8, 12)
        for i in range(num_vertices):
            angle = (i / num_vertices) * 2 * math.pi
            # Vary radius between 0.8 and 1.2 of original radius
            dist = self.radius * random.uniform(0.8, 1.2)
            x = math.cos(angle) * dist
            y = math.sin(angle) * dist
            self.vertices.append((x, y))
    
    @property
    def score_value(self):
        """Return score value based on asteroid size"""
        if self.radius >= ASTEROID_MIN_RADIUS * 3:
            return SCORE_LARGE
        elif self.radius >= ASTEROID_MIN_RADIUS * 2:
            return SCORE_MEDIUM
        return SCORE_SMALL
    
    def draw(self, screen):
        # Draw lumpy asteroid by connecting vertices
        points = []
        for x, y in self.vertices:
            point = (self.position.x + x, self.position.y + y)
            points.append(point)
        # Close the shape by connecting back to first point
        if points:
            points.append(points[0])
        pygame.draw.lines(screen, "white", False, points, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt
        self.wrap_position()
        
    def split(self):
        """Split asteroid into two smaller asteroids"""
        # Create explosion effect
        Explosion(self.position.x, self.position.y, self.radius)
        
        # If this is already a small asteroid, just destroy it
        if self.radius <= ASTEROID_MIN_RADIUS:
            self.kill()
            return
            
        # Calculate new properties for child asteroids
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        # Generate random split angle (20-50 degrees)
        split_angle = random.uniform(20, 50)
        
        # Create two new velocity vectors by rotating current velocity
        velocity1 = self.velocity.rotate(split_angle)
        velocity2 = self.velocity.rotate(-split_angle)
        
        # Create two new smaller asteroids
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        
        # Set their velocities (1.2x faster than parent)
        asteroid1.velocity = velocity1 * 1.2
        asteroid2.velocity = velocity2 * 1.2
        
        # Kill the original asteroid after creating the new ones
        self.kill()