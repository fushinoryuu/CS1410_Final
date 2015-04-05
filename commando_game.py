import pygame
import sys
import pyganim
from pygame.locals import *


def main():
    """This function will run the whole game."""
    pygame.init()

    # Define controls
    up = 'up'
    down = 'down'
    left = 'left'
    right = 'right'

    # Define the screen.
    screen_width = 640
    screen_height = 480
    display_surface = pygame.display.set_mode((screen_width, screen_height), 0, 32)
    pygame.display.set_caption('Commando!')

    # Load the background.
    background_image = pygame.image.load('gameimages/longBG.png')

    # Load the sprites
    front_standing = pygame.image.load('gameimages/crono_front.gif')
    back_standing = pygame.image.load('gameimages/crono_back.gif')
    left_standing = pygame.image.load('gameimages/crono_left.gif')
    right_standing = pygame.transform.flip(left_standing, True, False)
    player_width, player_height = front_standing.get_size()

    # Create the PygAnim objects for walking/running in all directions
    animation_types = 'back_run back_walk front_run front_walk left_run left_walk'.split()
    animation_objects = {}
    for animType in animation_types:
        images_and_durations = [('gameimages/crono_%s.%s.gif' % (animType, str(num).rjust(3, '0')), 0.1) for num in range(6)]
        animation_objects[animType] = pyganim.PygAnimation(images_and_durations)

    # Creates the right-facing sprites by copying the left ones.
    animation_objects['right_walk'] = animation_objects['left_walk'].getCopy()
    animation_objects['right_walk'].flip(True, False)
    animation_objects['right_walk'].makeTransformsPermanent()
    animation_objects['right_run'] = animation_objects['left_run'].getCopy()
    animation_objects['right_run'].flip(True, False)
    animation_objects['right_run'].makeTransformsPermanent()

    move_conductor = pyganim.PygConductor(animation_objects)

    # The player's default on spawn is facing down.
    direction = down

    basic_font = pygame.font.Font('freesansbold.ttf', 16)
    white = (255, 255, 255)
    background_color = (100, 50, 50)

    clock = pygame.time.Clock()
    player_x = 300
    player_y = 200
    walk_rate = 4
    run_rate = 12

    background_x = 0
    background_y = 0
    move_background = False

    instruction_surface = basic_font.render('Arrow keys to move. Hold shift to run.', True, white)
    instruction_rectangle = instruction_surface.get_rect()
    instruction_rectangle.bottomleft = (10, screen_height - 10)

    running = move_up = move_down = move_left = move_right = False

    while True:
        display_surface.blit(background_image, (background_x, background_y))
        for event in pygame.event.get():

            # Will handle exiting the program.
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == K_p:
                    # TODO Make it so the game is paused when the P key is pressed
                    pass

                if event.key in (K_LSHIFT, K_RSHIFT):
                    running = True

                if event.key == K_UP:
                    move_up = True
                    move_down = False
                    if not move_left and not move_right:
                        # Only change the direction to up if the player wasn't moving left/right
                        direction = up
                elif event.key == K_DOWN:
                    move_down = True
                    move_up = False
                    if not move_left and not move_right:
                        direction = down
                elif event.key == K_LEFT:
                    move_left = True
                    move_right = False
                    if not move_up and not move_down:
                        direction = left
                elif event.key == K_RIGHT:
                    move_right = True
                    move_left = False
                    if not move_up and not move_down:
                        direction = right

            elif event.type == KEYUP:
                if event.key in (K_LSHIFT, K_RSHIFT):
                    # The player has stopped running.
                    running = False

                if event.key == K_UP:
                    move_up = False

                    # If the player was moving in a sideways direction before, change the direction the player is facing.
                    if move_left:
                        direction = left
                    if move_right:
                        direction = right
                elif event.key == K_DOWN:
                    move_down = False
                    if move_left:
                        direction = left
                    if move_right:
                        direction = right
                elif event.key == K_LEFT:
                    move_left = False
                    if move_up:
                        direction = up
                    if move_down:
                        direction = down
                elif event.key == K_RIGHT:
                    move_right = False
                    if move_up:
                        direction = up
                    if move_down:
                        direction = down

        if move_up or move_down or move_left or move_right:
            # Draw the correct walking/running sprite from animation object
            move_conductor.play()
            if running:
                # Running
                if direction == up:
                    animation_objects['back_run'].blit(display_surface, (player_x, player_y))
                elif direction == down:
                    animation_objects['front_run'].blit(display_surface, (player_x, player_y))
                elif direction == left:
                    animation_objects['left_run'].blit(display_surface, (player_x, player_y))
                elif direction == right:
                    animation_objects['right_run'].blit(display_surface, (player_x, player_y))
            else:
                # Walking
                if direction == up:
                    animation_objects['back_walk'].blit(display_surface, (player_x, player_y))
                elif direction == down:
                    animation_objects['front_walk'].blit(display_surface, (player_x, player_y))
                elif direction == left:
                    animation_objects['left_walk'].blit(display_surface, (player_x, player_y))
                elif direction == right:
                    animation_objects['right_walk'].blit(display_surface, (player_x, player_y))

            # Actually move the position of the player.
            if running:
                rate = run_rate
            else:
                rate = walk_rate

            if move_up:
                player_y -= rate
            if move_down:
                player_y += rate
            if move_left:
                player_x -= rate
            if move_right:
                player_x += rate
                if move_background:
                    background_x -= rate

        else:
            # Standing still.
            move_conductor.stop()
            if direction == up:
                display_surface.blit(back_standing, (player_x, player_y))
            elif direction == down:
                display_surface.blit(front_standing, (player_x, player_y))
            elif direction == left:
                display_surface.blit(left_standing, (player_x, player_y))
            elif direction == right:
                display_surface.blit(right_standing, (player_x, player_y))

        # Make sure the player does move off the screen
        if player_x < 0:
            player_x = 0
        if player_x > screen_width - screen_width//3:
            if background_x > - screen_width:
                player_x = screen_width - screen_width//3
                move_background = True
            elif background_x <= - screen_width:
                background_x = - screen_width
                if player_x > screen_width - player_width:
                    player_x = screen_width - player_width
        else:
            move_background = False

        if player_y < 0:
            player_y = 0
        if player_y > screen_height - player_height:
            player_y = screen_height - player_height

        display_surface.blit(instruction_surface, instruction_rectangle)

        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    main()
    sys.exit()