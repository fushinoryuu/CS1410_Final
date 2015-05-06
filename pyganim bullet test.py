import pygame
from pygame.locals import *
import sys
import time
import pyganim



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

    def test(self):
        pass
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

pygame.init()

# define some constants
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# set up the window
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Pyganim Test 4')
# load long BG image
longBGimage = pygame.image.load('gameimages/longBG.png')

# load the "standing" sprites (these are single images, not animations)
front_standing = pygame.image.load('gameimages/player/soldier_front.png')
back_standing = pygame.image.load('gameimages/player/soldierBack.png')
left_standing = pygame.image.load('gameimages/player/soldier_left.png')
right_standing = pygame.transform.flip(left_standing, True, False)

playerWidth, playerHeight = front_standing.get_size()

# creating the PygAnimation objects for walking/running in all directions
animTypes = 'back_walk front_walk left_walk'.split()
#print(animTypes)
animObjs = {}
for animType in animTypes:
    imagesAndDurations = [('gameimages/player/soldier_%s.%s.png' % (animType, str(num).rjust(3, '0')), 0.1) for num in range(2)]
    animObjs[animType] = pyganim.PygAnimation(imagesAndDurations)

# create the right-facing sprites by copying and flipping the left-facing sprites
animObjs['right_walk'] = animObjs['left_walk'].getCopy()
animObjs['right_walk'].flip(True, False)
animObjs['right_walk'].makeTransformsPermanent()
#animObjs['right_run'] = animObjs['left_run'].getCopy()
#animObjs['right_run'].flip(True, False)
#animObjs['right_run'].makeTransformsPermanent()

moveConductor = pyganim.PygConductor(animObjs)
print(moveConductor)

direction = DOWN # player starts off facing down (front)

BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
WHITE = (255, 255, 255)
BGCOLOR = (100, 50, 50)
BLACK = (0, 0, 0)

mainClock = pygame.time.Clock()
x = 300 # x and y are the player's position
y = 400
WALKRATE = 6
RUNRATE = 12

xBG = 0
yBG = 0
moveBG = False

running = moveUp = moveDown = moveLeft = moveRight = False

all_sprites_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()

while True:
    # windowSurface.fill(BGCOLOR)
    windowSurface.blit(longBGimage, (xBG, yBG))
    for event in pygame.event.get(): # event handling loop

        # handle ending the program
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key in (K_LSHIFT, K_RSHIFT):
                # player has started running
                running = True

            if event.key == K_UP:
                moveUp = True
                moveDown = False
                if not moveLeft and not moveRight:
                    # only change the direction to up if the player wasn't moving left/right
                    direction = UP
            elif event.key == K_DOWN:
                moveDown = True
                moveUp = False
                if not moveLeft and not moveRight:
                    direction = DOWN
            elif event.key == K_LEFT:
                moveLeft = True
                moveRight = False
                if not moveUp and not moveDown:
                    direction = LEFT
            elif event.key == K_RIGHT:
                moveRight = True
                moveLeft = False
                if not moveUp and not moveDown:
                    direction = RIGHT

            elif event.key == K_SPACE:
                if direction == UP:
                    bullet = Bullet()
                    bullet.rect.x = (x + 25)
                    bullet.rect.y = y
                    all_sprites_list.add(bullet)
                    bullet_list.add(bullet)
                if direction == DOWN:
                    bullet = downBullet()
                    bullet.rect.x = (x + 25)
                    bullet.rect.y = (y + 30)
                    all_sprites_list.add(bullet)
                    bullet_list.add(bullet)
                if direction == LEFT:
                    bullet = leftBullet()
                    bullet.rect.x = (x + 25)
                    bullet.rect.y = (y + 30)
                    all_sprites_list.add(bullet)
                    bullet_list.add(bullet)
                if direction == RIGHT:
                    bullet = rightBullet()
                    bullet.rect.x = (x + 25)
                    bullet.rect.y = (y + 30)
                    all_sprites_list.add(bullet)
                    bullet_list.add(bullet)






        elif event.type == KEYUP:
            if event.key in (K_LSHIFT, K_RSHIFT):
                # player has stopped running
                running = False

            if event.key == K_UP:
                moveUp = False
                # if the player was moving in a sideways direction before, change the direction the player is facing.
                if moveLeft:
                    direction = LEFT
                if moveRight:
                    direction = RIGHT
            elif event.key == K_DOWN:
                moveDown = False
                if moveLeft:
                    direction = LEFT
                if moveRight:
                    direction = RIGHT
            elif event.key == K_LEFT:
                moveLeft = False
                if moveUp:
                    direction = UP
                if moveDown:
                    direction = DOWN
            elif event.key == K_RIGHT:
                
                moveRight = False
                if moveUp:
                    direction = UP
                if moveDown:
                    direction = DOWN
    for bullet in bullet_list:
        if bullet.rect.y < -10 or bullet.rect.y > 500 or bullet.rect.x < -10 or bullet.rect.x > 650:
            print('off screen')
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)


    if moveUp or moveDown or moveLeft or moveRight:
        # draw the correct walking/running sprite from the animation object
        moveConductor.play() # calling play() while the animation objects are already playing is okay; in that case play() is a no-op
        if running:
            if direction == UP:
                animObjs['back_run'].blit(windowSurface, (x, y))
            elif direction == DOWN:
                animObjs['front_run'].blit(windowSurface, (x, y))
            elif direction == LEFT:
                animObjs['left_run'].blit(windowSurface, (x, y))
            elif direction == RIGHT:
                animObjs['right_run'].blit(windowSurface, (x, y))
        else:
            # walking
            if direction == UP:
                animObjs['back_walk'].blit(windowSurface, (x, y))
            elif direction == DOWN:
                animObjs['front_walk'].blit(windowSurface, (x, y))
            elif direction == LEFT:
                animObjs['left_walk'].blit(windowSurface, (x, y))
            elif direction == RIGHT:
                animObjs['right_walk'].blit(windowSurface, (x, y))


        # actually move the position of the player
        if running:
            rate = RUNRATE
        else:
            rate = WALKRATE

        if moveUp:
            y -= rate
        if moveDown:
            y += rate
        if moveLeft:
            x -= rate
        if moveRight:
            x += rate
            if moveBG:
                xBG -= rate
        

    else:
        # standing still
        moveConductor.stop() # calling stop() while the animation objects are already stopped is okay; in that case stop() is a no-op
        if direction == UP:
            windowSurface.blit(back_standing, (x, y))
        elif direction == DOWN:
            windowSurface.blit(front_standing, (x, y))
        elif direction == LEFT:
            windowSurface.blit(left_standing, (x, y))
        elif direction == RIGHT:
            windowSurface.blit(right_standing, (x, y))

    # make sure the player does move off the screen
    if x < 0:
        x = 0
##    if x > WINDOWWIDTH - playerWidth:
##        x = WINDOWWIDTH - playerWidth
    if x > WINDOWWIDTH - WINDOWWIDTH//3:
        if xBG > - WINDOWWIDTH:
            x = WINDOWWIDTH - WINDOWWIDTH//3
            moveBG = True
        elif xBG <= - WINDOWWIDTH: 
            xBG = - WINDOWWIDTH
            if x > WINDOWWIDTH - playerWidth:
                x = WINDOWWIDTH - playerWidth
    else:
        moveBG = False
        
    if y < 0:
        y = 0
    if y > WINDOWHEIGHT - playerHeight:
        y = WINDOWHEIGHT - playerHeight

    all_sprites_list.update()
    all_sprites_list.draw(windowSurface)
    pygame.display.update()
    mainClock.tick(30) # Feel free to experiment with any FPS setting.
