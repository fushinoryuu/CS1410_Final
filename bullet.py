import pygame
from pygame.locals import *

pygame.init()


class upBullet(pygame.sprite.Sprite):
    """This class represents the bullet that travels up."""
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load('gameimages/player/bulletImage.png')
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.y -= 7


class downBullet(pygame.sprite.Sprite):
    """This class represents the bullet that travels down."""
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load('gameimages/player/bulletImage.png')
        self.image = pygame.transform.flip(self.image, False, True)

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.y += 7


class leftBullet(pygame.sprite.Sprite):
    """This class represents the bullet that travels left."""
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load('gameimages/player/bulletImage.png')
        self.image = pygame.transform.rotate(self.image, +90)

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.x -= 7


class rightBullet(pygame.sprite.Sprite):
    """This class represents the bullet that travels right."""
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load('gameimages/player/bulletImage.png')
        self.image = pygame.transform.rotate(self.image, -90)

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.x += 7