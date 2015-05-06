import pygame
import sys
import pyganim
from pygame.locals import *
from game_interface import GameInterface
from random import randint
from bullet import Bullet, downBullet, leftBullet, rightBullet
from enemy_class import Enemy

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
game_interface = GameInterface()
click_start = pygame.mixer.Sound('sound/DoubleGunshot.wav')
walking = pygame.mixer.Sound('sound/Walking.wav')
menu_music = pygame.mixer.music.load('sound/bensound-extremeaction.ogg')
walking.set_volume(.8)
click_start.set_volume(1)
pygame.mixer.music.set_volume(.07)

def game():
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

    # Load images
    background_game = pygame.image.load('gameimages/crackeddirt.png')

    # Load the player sprites
    front_standing = pygame.image.load('gameimages/player/soldier_front.png')
    back_standing = pygame.image.load('gameimages/player/soldierBack.png')
    left_standing = pygame.image.load('gameimages/player/soldier_left.png')
    right_standing = pygame.transform.flip(left_standing, True, False)
    player_width, player_height = front_standing.get_size()


    # Load the enemy sprites
    #enemy_left = pygame.image.load('gameimages/enemies/enemy_front.gif')

    # Create the PygAnim objects for walking/running in all directions
    animation_types = 'back_walk front_walk left_walk'.split()
    animation_objects = {}
    for animType in animation_types:
        images_and_durations = [('gameimages/player/soldier_%s.%s.png' %
                                 (animType, str(num).rjust(3, '0')), 0.1) for num in range(2)]
        animation_objects[animType] = pyganim.PygAnimation(images_and_durations)

    """enemy_types = 'left_walk'.split()
    enemy_objects = {}
    for animType in enemy_types:
        images_and_durations = [('gameimages/enemies/enemy_%s.%s.gif' %
                                 (animType, str(num).rjust(3, '0')), 0.1) for num in range(2)]
        enemy_objects[animType] = pyganim.PygAnimation(images_and_durations)"""

    # Creates the right-facing sprites by copying the left ones.
    animation_objects['right_walk'] = animation_objects['left_walk'].getCopy()
    animation_objects['right_walk'].flip(True, False)
    animation_objects['right_walk'].makeTransformsPermanent()


    move_conductor = pyganim.PygConductor(animation_objects)
    #enemy_conductor = pyganim.PygConductor(enemy_objects)

    # The player's default on spawn is facing down.
    direction = down

    clock = pygame.time.Clock()
    player_x = 300
    player_y = 200

    walk_rate = 6
    run_rate = 12

    """enemy_x = 100
    enemy_y = 100"""

    background_x = 0
    background_y = 0
    move_background = False

    running = move_up = move_down = move_left = move_right = False

    all_sprites_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()
    enemy_list = pygame.sprite.Group()

    enemy = Enemy((400, 100), display_surface)
    enemy_list.add(enemy)
    all_sprites_list.add(enemy)

    while True:
        display_surface.blit(background_game, (background_x, background_y))
        """enemy_conductor.play()
        enemy_objects['left_walk'].blit(display_surface, (enemy_x, enemy_y))"""

        for event in pygame.event.get():


            # Will handle exiting the program.
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == K_RETURN:
                    main()



                if event.key == K_UP:
                    move_up = True
                    move_down = False
                    walking.play()
                    if not move_left and not move_right:
                        # Only change the direction to up if the player wasn't moving left/right
                        direction = up
                elif event.key == K_DOWN:
                    move_down = True
                    move_up = False
                    walking.play()
                    if not move_left and not move_right:
                        direction = down
                elif event.key == K_LEFT:
                    move_left = True
                    move_right = False
                    walking.play()
                    if not move_up and not move_down:
                        direction = left
                elif event.key == K_RIGHT:
                    move_right = True
                    move_left = False
                    walking.play()
                    if not move_up and not move_down:
                        direction = right
                elif event.key == K_SPACE:
                    if direction == up:
                        bullet = Bullet()
                        bullet.rect.x = (player_x + 25)
                        bullet.rect.y = player_y
                        all_sprites_list.add(bullet)
                        bullet_list.add(bullet)
                    if direction == down:
                        bullet = downBullet()
                        bullet.rect.x = (player_x + 25)
                        bullet.rect.y = (player_y + 30)
                        all_sprites_list.add(bullet)
                        bullet_list.add(bullet)
                    if direction == left:
                        bullet = leftBullet()
                        bullet.rect.x = (player_x + 25)
                        bullet.rect.y = (player_y + 30)
                        all_sprites_list.add(bullet)
                        bullet_list.add(bullet)
                    if direction == right:
                        bullet = rightBullet()
                        bullet.rect.x = (player_x + 25)
                        bullet.rect.y = (player_y + 30)
                        all_sprites_list.add(bullet)
                        bullet_list.add(bullet)

            elif event.type == KEYUP:


                if event.key == K_UP:
                    move_up = False
                    walking.stop()

                    # If the player was moving in a sideways direction before, change the direction the player is facing
                    if move_left:
                        direction = left
                    if move_right:
                        direction = right
                elif event.key == K_DOWN:
                    move_down = False
                    walking.stop()
                    if move_left:
                        direction = left
                    if move_right:
                        direction = right
                elif event.key == K_LEFT:
                    move_left = False
                    walking.stop()
                    if move_up:
                        direction = up
                    if move_down:
                        direction = down
                elif event.key == K_RIGHT:
                    move_right = False
                    walking.stop()
                    if move_up:
                        direction = up
                    if move_down:
                        direction = down

        for bullet in bullet_list:
            if bullet.rect.y < -10 or bullet.rect.y > 500 or bullet.rect.x < -10 or bullet.rect.x > 650:
                print('off screen')
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)

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
                if move_background:
                    background_y += rate
            if move_down:
                player_y += rate
                if move_background:
                    background_y -= rate
            if move_left:
                player_x -= rate
                if move_background:
                    background_x += rate
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
        if player_x > screen_width - screen_width // 3:
            if background_x > - screen_width:
                player_x = screen_width - screen_width // 3
                move_background = True
            elif background_x <= - screen_width:
                background_x = - screen_width
                if player_x > screen_width - player_width:
                    player_x = screen_width - player_width

        else:
            move_background = False

        if player_y < 0:
            player_y = 0
        if player_y > screen_height - screen_height // 3:
            if background_y > - screen_height:
                player_y = screen_height - screen_height // 3
                move_background = True
            elif background_y <= - screen_height:
                background_y = - screen_height
                if player_y > screen_height - player_height:
                    player_y = screen_height - player_height

        all_sprites_list.update()
        all_sprites_list.draw(display_surface)
        print(player_x, player_y)
        pygame.display.update()

        # Collision variable(Makes the Orange square collide with the Purple ones)
        #squaresHITlist = pygame.sprite.spritecollide(player, squareList, True)
        clock.tick(30)


def main():
    """This function runs the main menu for the game."""
    game_interface.start_setup()

    while True:
        for event in pygame.event.get():
            game_interface.all_buttons_active()

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                mouse_xy = pygame.mouse.get_pos()

                if game_interface.start_button.clicked(mouse_xy):
                    game_interface.start_button.highlighted = True
                    click_start.play()
                    pygame.mixer.music.play(-1)
                elif game_interface.quit_button.clicked(mouse_xy):
                    click_start.play()
                    game_interface.quit_button.highlighted = True
                elif game_interface.credits_button.clicked(mouse_xy):
                    game_interface.credits_button.highlighted = True
                    click_start.play()

            elif event.type == MOUSEBUTTONUP:
                if game_interface.start_button.clicked(mouse_xy):
                    game_interface.start_button.highlighted = False
                    game()
                elif game_interface.quit_button.clicked(mouse_xy):
                    pygame.quit()
                    sys.exit()
                elif game_interface.credits_button.clicked(mouse_xy):
                    game_interface.status = 1
                    game_interface.credits_button.highlighted = False
        game_interface.display_interface()
        pygame.display.update()


if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()