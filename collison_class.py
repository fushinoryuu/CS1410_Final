__author__ = 'Steve'

## This is complete, some of this will need to be added to the main function to get the squares
## to blit.
import pygame, sys
from pygame.locals import *
from random import randrange

FPS = 60
SQSIZE = 25

enemy = 5

PURPLE = (100, 10, 175)
ORANGE = (230, 100, 25)
screen_width = 640
screen_height = 480

class Square(pygame.sprite.Sprite):

    def __init__(self, color, width, height):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

    def resizeSQ(self, x, y):
        self.image = pygame.transform.scale(self.image, (x, y))
        self.rect = self.image.get_rect()


    def squareList(self):
        self.squareList = pygame.sprite.Group()
        self.allSPRITESlist = pygame.sprite.Group()

        for i in range(enemy):
            square = Square(PURPLE, SQSIZE, SQSIZE)
            square.rect.x = randrange(SQSIZE, screen_width) - SQSIZE
            square.rect.y = randrange(SQSIZE, screen_height) - SQSIZE
            self.squareList.add(square)
            self.allSPRITESlist.add(square)


#These plus a few more above need to go into main
#clock = pygame.time.Clock()
#squaresHITlist = pygame.sprite.spritecollide(enemy, squareList, True)
#allSPRITESlist.draw(display_surface)

#pygame.display.flip()

#clock.tick(FPS)

