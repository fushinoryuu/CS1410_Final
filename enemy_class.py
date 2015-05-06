import pygame
from pygame.locals import *

pygame.init()

class Enemy(pygame.sprite.Sprite):
    """This class represents the enemy unit."""
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(Enemy, self).__init__()

        self.image = pygame.image.load('gameimages/enemies/enemy_front.gif')
        self.rect = self.image.get_rect()

class Crate(pygame.sprite.Sprite):
    """This class represents a crate."""
    def __init__(self):
        super(Crate, self).__init__()

        self.image = pygame.image.load('gameimages/enemies/crate.gif')
        self.rect = self.image.get_rect()