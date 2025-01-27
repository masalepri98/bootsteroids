import pygame
import random
import math
from constants import EXPLOSION_DURATION, EXPLOSION_PARTICLES, EXPLOSION_SPEED

class Explosion:
    containers = []  # Will be set from main.py
    
    def __init__(self, x: int, y: int, radius: float):
        self.position = pygame.Vector2(x, y)
        self.particles = []
        self.timer = EXPLOSION_DURATION
        
        # Create particles
        for _ in range(EXPLOSION_PARTICLES):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(EXPLOSION_SPEED * 0.5, EXPLOSION_SPEED)
            velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
            self.particles.append({
                'pos': pygame.Vector2(x, y),
                'vel': velocity,
                'size': random.uniform(1, 3)
            })
            
        # Add self to containers
        for container in self.containers:
            container.append(self)
    
    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.kill()
            return
            
        # Update particle positions
        for particle in self.particles:
            particle['pos'] += particle['vel'] * dt
            particle['vel'] *= 0.95  # Slow down over time
    
    def draw(self, screen):
        # Fade out based on remaining time
        alpha = int((self.timer / EXPLOSION_DURATION) * 255)
        
        # Draw each particle
        for particle in self.particles:
            pos = particle['pos']
            size = particle['size']
            # Create a surface for the particle with transparency
            particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (255, 255, 255, alpha), 
                             (size, size), size)
            screen.blit(particle_surface, pos - pygame.Vector2(size, size))
    
    def kill(self):
        for container in self.containers:
            if self in container:
                container.remove(self) 