__author__ = 'Steve'

## This is complete, some of this will need to be added to the main function to get the squares
## to blit.
import pygame
from pygame.locals import *
from random import randrange

class Square(pygame.sprite.Sprite):

    def __init__(self, color, width, height):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

    def __resizeSQ(self, x, y):
        self.image = pygame.transform.scale(self.image, (x, y))
        self.rect = self.image.get_rect()


