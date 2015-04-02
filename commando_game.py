import pygame
import sys
from pygame.locals import *


def main():
    """This function will run the whole game."""
    pygame.init()

    screen_size = (1280, 720)
    grey = (192, 192, 192)

    display_surface = pygame.display.set_mode((screen_size[0], screen_size[1]), 0, 32)
    pygame.display.set_caption('Commando!')

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        display_surface.fill(grey)
        pygame.display.update()

if __name__ == "__main__":
    main()
    sys.exit()