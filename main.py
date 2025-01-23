# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
import sys
from constants import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Bootsteroids")
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        screen.fill("black")
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()