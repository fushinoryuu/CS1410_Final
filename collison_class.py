import pygame
from pygame.locals import *

class Collision(pygame.sprite.Sprite):

    def __init__(self, width, height):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()

    def __resizeSQ(self, x, y):
        self.image = pygame.transform.scale(self.image, (x, y))
        self.rect = self.image.get_rect()