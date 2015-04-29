__author__ = 'Steve'

## Wanted to get some of this typed up to add in, will be working on it more in the next few days.
import pygame, sys
from pygame.locals import *
from random import randrange

FPS = 60
SQSIZE = 25

class Square(pygame.sprite.Sprite):

    def __init__(self, color, width, height):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

    def resizeSQ(self, x, y):
        self.image = pygame.transform.scale(self.image, (x, y))
        self.rect = self.image.get_rect()

enemy = 30

squareList = pygame.sprite.Group()

allSPRITESlist = pygame.sprite.Group()

for i in range(enemy):
    square = Square(PURPLE, SQSIZE, SQSIZE)

    square.rect.x = randrange(SQSIZE, DWIDTH ) - SQSIZE
    square.rect.y = randrange(SQSIZE, DHEIGHT) - SQSIZE

    squareList.add(square)
    allSPRITESlist.add(square)

player = Square(ORANGE, 30, 30)
allSPRITESlist.add(player)

