import pygame
import random
from asteroid import Asteroid
from constants import *


class AsteroidField:
    containers = []  # Will be set from main.py
    
    def __init__(self):
        # Add self to containers (updatable group)
        for container in self.containers:
            container.append(self)
        self.spawn_timer = 0
    
    def update(self, dt):
        self.spawn_timer += dt
        
        # Spawn a new asteroid every ASTEROID_SPAWN_DELAY seconds
        if self.spawn_timer >= ASTEROID_SPAWN_DELAY:
            self.spawn_timer = 0
            self.spawn_asteroid()
    
    def spawn_asteroid(self):
        # Random position along screen edge
        side = random.randint(0, 3)
        if side == 0:  # Top
            x = random.randint(0, SCREEN_WIDTH)
            y = 0
        elif side == 1:  # Right
            x = SCREEN_WIDTH
            y = random.randint(0, SCREEN_HEIGHT)
        elif side == 2:  # Bottom
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT
        else:  # Left
            x = 0
            y = random.randint(0, SCREEN_HEIGHT)
            
        # Create asteroid with random size and velocity
        asteroid = Asteroid(x, y, random.randint(ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS))
        asteroid.velocity = pygame.Vector2(
            random.uniform(-ASTEROID_MAX_SPEED, ASTEROID_MAX_SPEED),
            random.uniform(-ASTEROID_MAX_SPEED, ASTEROID_MAX_SPEED)
        )