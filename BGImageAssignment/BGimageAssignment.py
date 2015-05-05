#BGmoveAssignment
#Steven Sauter
#2/25/2015

import pygame, sys
from pygame.locals import *

#BG Image is 1920 x 1080
BGimageFileName = 'planetearth.jpg'
SPRITE01FileName = 'astronaut256.tga'

pygame.init()

#Global Variables
DWIDTH = 800
DHEIGHT = 600
MOVESPEED = 8
ROTATESPEED = 5.0
SPApos = (DWIDTH//2, DHEIGHT//2 )
SPArot = 0
DISPLAYSURF = pygame.display.set_mode((DWIDTH, DHEIGHT), 0, 32)
BGimage = pygame.image.load(BGimageFileName).convert()
SpAstronaut = pygame.image.load(SPRITE01FileName).convert_alpha()

#Main Fuction. To move astronaut use arrow keys. To rotate use W and R.

def main():

    x, y = 0, 0
    move_x, move_y = 0, 0

    rotationDIR = 0
    spriteROT = 0

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    move_x = MOVESPEED
                elif event.key == K_RIGHT:
                    move_x = -MOVESPEED
                elif event.key == K_UP:
                    move_y = MOVESPEED
                elif event.key == K_DOWN:
                    move_y = -MOVESPEED
                elif event.key == K_r:
                    rotationDIR = - ROTATESPEED
                elif event.key == K_w:
                    rotationDIR = + ROTATESPEED

            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    move_x = 0
                elif event.key == K_RIGHT:
                    move_x = 0
                elif event.key == K_UP:
                    move_y = 0
                elif event.key == K_DOWN:
                    move_y = 0
                elif event.key == K_r:
                    rotationDIR = 0
                elif event.key == K_w:
                    rotationDIR = 0

            x += move_x
            y += move_y
            spriteROT += rotationDIR

            if x >= 0:
                x = 0
            if y >= 0:
                y = 0
            if x <= -1 * (DWIDTH * 2 - DWIDTH):
                x = -1 * (DWIDTH * 2 - DWIDTH)
            if y <= -1 * (DHEIGHT * 2 - DHEIGHT):
                y = -1 * (DHEIGHT * 2 - DHEIGHT)

        DISPLAYSURF.blit(BGimage, (-500, -500))

        RotSPA = pygame.transform.rotate(pygame.transform.scale(SpAstronaut, (DWIDTH//4, DWIDTH//4)), spriteROT)
        w, h = RotSPA.get_size()
        spriteDrawPos = (SPApos[0] - w // 2, SPApos[1] - h // 2)

        DISPLAYSURF.blit(RotSPA, spriteDrawPos)

        pygame.display.update()

main()

            
                

