from circleshape import CircleShape
from constants import (PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, 
                      PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN, STARTING_LIVES, RESPAWN_TIME,
                      PLAYER_ACCELERATION, PLAYER_FRICTION)
import pygame
from shot import Shot
import random

class Player(CircleShape):
    def __init__(self, x: int, y: int):
        # Call parent constructor with position and player radius
        super().__init__(x, y, PLAYER_RADIUS)
        # Initialize rotation to 0
        self.rotation = 0
        # Initialize shoot cooldown timer
        self.shoot_timer = 0
        self.lives = STARTING_LIVES
        self.respawn_timer = 0
        self.is_vulnerable = True
        self.initial_position = pygame.Vector2(x, y)
        # Add velocity for acceleration-based movement
        self.velocity = pygame.Vector2(0, 0)
        # Thruster particles
        self.thrusting = False
        self.thrust_particles = []
    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = pygame.Vector2(self.position + forward * self.radius)
        b = pygame.Vector2(self.position - forward * self.radius - right)
        c = pygame.Vector2(self.position - forward * self.radius + right)
        return [a, b, c]

    def draw(self, screen):
        # Draw thrust particles
        if self.thrust_particles:
            for particle in self.thrust_particles:
                alpha = int((particle['life'] / 0.3) * 255)  # Fade out
                particle_surface = pygame.Surface((3, 3), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, (255, 255, 255, alpha), 
                                 (1.5, 1.5), 1.5)
                screen.blit(particle_surface, particle['pos'] - pygame.Vector2(1.5, 1.5))
        
        # Draw ship
        if self.is_vulnerable or pygame.time.get_ticks() % 200 < 100:
            pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def update(self, dt):
        # Handle respawn timer
        if not self.is_vulnerable:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0:
                self.is_vulnerable = True
        
        # Decrease shoot timer
        if self.shoot_timer > 0:
            self.shoot_timer -= dt
        
        keys = pygame.key.get_pressed()
        self.thrusting = False
        
        if keys[pygame.K_a]:
            self.rotate(-dt)  # Negative dt for counter-clockwise rotation
        if keys[pygame.K_d]:
            self.rotate(dt)   # Positive dt for clockwise rotation
            
        if keys[pygame.K_w]:
            self.thrust(dt)     # Forward movement with acceleration
            self.thrusting = True
        
        if keys[pygame.K_s]:
            self.move(-dt)    # Backward movement

        # Apply friction/drag
        self.velocity *= PLAYER_FRICTION
        
        # Update position based on velocity
        self.position += self.velocity * dt
        
        # Update thrust particles
        for particle in self.thrust_particles[:]:
            particle['life'] -= dt
            if particle['life'] <= 0:
                self.thrust_particles.remove(particle)
            else:
                particle['pos'] += particle['vel'] * dt
        
        # Handle shooting
        if keys[pygame.K_SPACE] and self.shoot_timer <= 0:
            self.shoot()
            
        # Wrap position around screen edges
        self.wrap_position()

    def move(self, dt):
        # Create upward-pointing unit vector (0, 1)
        direction = pygame.Vector2(0, 1)
        # Rotate it by player's current rotation
        direction = direction.rotate(self.rotation)
        # Scale by speed and dt
        movement = direction * PLAYER_SPEED * dt
        # Update position
        self.position += movement

    def shoot(self):
        """Creates a new shot moving in the direction the player is facing"""
        # Create shot at player position
        shot = Shot(self.position.x, self.position.y)
        # Set velocity in direction player is facing (same as movement direction)
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = direction * PLAYER_SHOOT_SPEED
        # Reset shoot timer
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN

    def respawn(self):
        """Reset player position and start invulnerability timer"""
        self.lives -= 1
        if self.lives >= 0:  # Only respawn if we have lives remaining
            self.position = self.initial_position.copy()
            self.velocity = pygame.Vector2(0, 0)
            self.rotation = 0
            self.respawn_timer = RESPAWN_TIME
            self.is_vulnerable = False

    def collides_with(self, other: 'CircleShape') -> bool:
        """Override circle collision with triangle collision for player"""
        # Get the triangle points for collision checking
        triangle_points = self.triangle()
        
        # If other object is an asteroid (circle), check if any point of the triangle
        # is within the circle, or if the circle intersects any of the triangle's lines
        if hasattr(other, 'radius'):  # Checking if it's a circle-based object
            # Check if circle center is inside triangle
            if pygame.math.Vector2(other.position).distance_to(self.position) <= other.radius:
                return True
                
            # Check each line of the triangle against the circle
            for i in range(3):
                point1 = triangle_points[i]
                point2 = triangle_points[(i + 1) % 3]
                
                # Calculate closest point on line to circle center
                line_vec = point2 - point1
                line_len = line_vec.length()
                if line_len == 0:
                    continue
                    
                line_unit = line_vec / line_len
                point_to_circle = other.position - point1
                projection_len = max(0, min(line_len, point_to_circle.dot(line_unit)))
                closest_point = point1 + line_unit * projection_len
                
                # Check if closest point is within circle radius
                if closest_point.distance_to(other.position) <= other.radius:
                    return True
                    
        return False

    def thrust(self, dt):
        # Apply acceleration in facing direction
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += direction * PLAYER_ACCELERATION * dt
        
        # Add thrust particles
        if random.random() < 0.5:  # Only add particles sometimes for variation
            # Calculate thruster position (back of ship)
            back_pos = self.position - direction * self.radius
            spread = 20  # Spread angle in degrees
            angle = self.rotation + 180 + random.uniform(-spread, spread)
            speed = random.uniform(100, 200)
            vel = pygame.Vector2(0, 1).rotate(angle) * speed
            
            self.thrust_particles.append({
                'pos': back_pos.copy(),
                'vel': vel,
                'life': random.uniform(0.1, 0.3)
            })