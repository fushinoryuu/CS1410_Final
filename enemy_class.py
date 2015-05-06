import pygame
from pygame.locals import *

pygame.init()

class Enemy(pygame.sprite.Sprite):
    """This class represents the enemy unit."""
    def __init__(self, surface):
        # Call the parent class (Sprite) constructor
        super(Enemy, self).__init__()

        self.image = pygame.image.load('gameimages/enemies/enemy_front.gif')
        self.rect = self.image.get_rect()
        # self.surface = surface
        #
        # self.position = position

    # def update(self):
    #     self.surface.blit(self.image, self.position)