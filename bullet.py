import pygame
from pygame.locals import *

pygame.init()

class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load('gameimages/player/bulletImage.png')
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.y -= 7
class downBullet(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load('gameimages/player/bulletImage.png')
        self.image = pygame.transform.flip(self.image, False, True)

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.y += 7

    def test(self):
        pass

class leftBullet(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load('gameimages/player/bulletImage.png')
        self.image = pygame.transform.rotate(self.image, +90)

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.x -= 7

    def test(self):
        pass
class rightBullet(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.image.load('gameimages/player/bulletImage.png')
        self.image = pygame.transform.rotate(self.image, -90)

        self.rect = self.image.get_rect()

    def update(self):
        """ Move the bullet. """
        self.rect.x += 7

    def test(self):
        pass