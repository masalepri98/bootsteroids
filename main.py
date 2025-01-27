# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion

def reset_game():
    """Create and return fresh game objects and initial score"""
    # Create groups to manage game objects
    updatable = []
    drawable = []
    asteroids = []
    shots = []
    explosions = []
    
    # Set up containers before creating objects
    Asteroid.containers = [asteroids, updatable, drawable]
    Shot.containers = [shots, updatable, drawable]
    AsteroidField.containers = [updatable]
    Explosion.containers = [explosions, updatable, drawable]
    
    # Create game objects
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    updatable.append(player)
    drawable.append(player)
    
    return {
        'updatable': updatable,
        'drawable': drawable,
        'asteroids': asteroids,
        'shots': shots,
        'player': player,
        'asteroid_field': asteroid_field,
        'score': 0,
        'explosions': explosions,
    }

def draw_game_over(screen, score, font):
    """Draw game over screen with score and options"""
    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(128)
    screen.blit(overlay, (0, 0))
    
    # Game Over text
    game_over_text = font.render("GAME OVER!", True, "white")
    score_text = font.render(f"Final Score: {score}", True, "white")
    retry_text = font.render("Press SPACE to play again", True, "white")
    quit_text = font.render("Press ESC to quit", True, "white")
    
    # Center all text
    screen_center_x = SCREEN_WIDTH // 2
    screen_center_y = SCREEN_HEIGHT // 2
    
    screen.blit(game_over_text, 
                game_over_text.get_rect(centerx=screen_center_x, centery=screen_center_y - 60))
    screen.blit(score_text, 
                score_text.get_rect(centerx=screen_center_x, centery=screen_center_y))
    screen.blit(retry_text, 
                retry_text.get_rect(centerx=screen_center_x, centery=screen_center_y + 60))
    screen.blit(quit_text, 
                quit_text.get_rect(centerx=screen_center_x, centery=screen_center_y + 100))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Bootsteroids")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    
    # Create game objects and get containers
    game_objects = reset_game()
    game_over = False
    
    running = True
    while running:
        dt = clock.tick(60) / 1000  # Update delta time
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_SPACE:
                    # Reset game
                    game_objects = reset_game()
                    game_over = False
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        # Game logic and drawing
        screen.fill("black")
        
        if not game_over:
            # Update all objects
            for obj in game_objects['updatable']:
                obj.update(dt)
                
            # Draw score and lives
            score_text = font.render(f"Score: {game_objects['score']}", True, "white")
            lives_text = font.render(f"Lives: {game_objects['player'].lives}", True, "white")
            screen.blit(score_text, (10, 10))
            screen.blit(lives_text, (10, 50))
            
            # Check for collisions between player and asteroids
            for asteroid in game_objects['asteroids']:
                if game_objects['player'].is_vulnerable and game_objects['player'].collides_with(asteroid):
                    game_objects['player'].respawn()
                    if game_objects['player'].lives < 0:
                        game_over = True
                        # Stop updating player to prevent further movement
                        game_objects['updatable'].remove(game_objects['player'])
                    break
                
                # Check for collisions between shots and asteroids
                for shot in game_objects['shots'][:]:
                    if shot.collides_with(asteroid):
                        game_objects['score'] += asteroid.score_value
                        shot.kill()
                        asteroid.split()
                        break
            
            # Draw all objects
            for obj in game_objects['drawable']:
                obj.draw(screen)
        else:
            # Draw game over screen
            for obj in game_objects['drawable']:
                obj.draw(screen)  # Draw final game state in background
            draw_game_over(screen, game_objects['score'], font)
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()