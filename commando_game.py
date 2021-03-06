import pygame
import sys
import pyganim
import random
from pygame.locals import *
from game_interface import GameInterface
from bullet import upBullet, downBullet, leftBullet, rightBullet
from collidable import Enemy, Crate, Goal, Player

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
game_interface = GameInterface()

# Load all the sound effects we use in the game.
click_start = pygame.mixer.Sound('sound/RifleshotV2.wav')
walking = pygame.mixer.Sound('sound/Walking.wav')
gunshot = pygame.mixer.Sound('sound/Gunshot.wav')
deathsound = pygame.mixer.Sound('sound/deathsound.wav')
breaksound = pygame.mixer.Sound('sound/DebrisHit.wav')
game_music = pygame.mixer.music.load('sound/bensound-extremeaction.ogg')
deathsound.set_volume(.5)
breaksound.set_volume(1)
gunshot.set_volume(.6)
walking.set_volume(.8)
click_start.set_volume(.2)
pygame.mixer.music.set_volume(.07)

def end():
    """This function runs the end of the game once the goal is reached."""
    game_interface.all_buttons_inactive()
    pygame.mixer.music.stop()

    while True:
        for event in pygame.event.get():
            game_interface.final()

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
        game_interface.final()
        pygame.display.update()

def game():
    """This function runs the main game."""

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
    background_game = pygame.image.load('gameimages/rev_crackeddirt.png')

    # Load the player sprites
    front_standing = pygame.image.load('gameimages/player/soldier_front.png')
    back_standing = pygame.image.load('gameimages/player/soldierBack.png')
    left_standing = pygame.image.load('gameimages/player/soldier_left.png')
    right_standing = pygame.transform.flip(left_standing, True, False)
    player_width, player_height = front_standing.get_size()

    # Create the PygAnim objects for walking/running in all directions
    animation_types = 'back_walk front_walk left_walk'.split()
    animation_objects = {}
    for animType in animation_types:
        images_and_durations = [('gameimages/player/soldier_%s.%s.png' %
                                 (animType, str(num).rjust(3, '0')), 0.1) for num in range(2)]
        animation_objects[animType] = pyganim.PygAnimation(images_and_durations)

    # Creates the right-facing sprites by copying the left ones.
    animation_objects['right_walk'] = animation_objects['left_walk'].getCopy()
    animation_objects['right_walk'].flip(True, False)
    animation_objects['right_walk'].makeTransformsPermanent()

    # Creates the right-facing sprites by copying the left ones.
    animation_objects['right_walk'] = animation_objects['left_walk'].getCopy()
    animation_objects['right_walk'].flip(True, False)
    animation_objects['right_walk'].makeTransformsPermanent()

    # Creates the animations for the crates breaking.
    crate_types = 'break'.split()
    crate_animations = {}
    for animType in crate_types:
        images_and_durations = [('gameimages/enemies/crate_%s.%s.gif' %
                                 (animType, str(num).rjust(3, '0')), .5) for num in range(2)]
        crate_animations[animType] = pyganim.PygAnimation(images_and_durations)

    # Creates the animations for the helicopter/goal.
    goal_types = 'goal'.split()
    goal_animations = {}
    for animType in goal_types:
        images_and_durations = [('gameimages/player/helicopter_%s.%s.gif' %
                                 (animType, str(num).rjust(3, '0')), .1) for num in range(5)]
        goal_animations[animType] = pyganim.PygAnimation(images_and_durations)

    move_conductor = pyganim.PygConductor(animation_objects)
    goal_conductor = pyganim.PygConductor(goal_animations)

    # The player's default on spawn is facing down.
    direction = down

    clock = pygame.time.Clock()
    player_x = 300
    player_y = 200

    walk_rate = 6
    run_rate = 12

    background_x = -100
    background_y = -100
    move_background = False

    running = move_up = move_down = move_left = move_right = False

    # Creates all the sprite groups for collision.
    all_sprites_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()
    enemy_list = pygame.sprite.Group()
    crate_list = pygame.sprite.Group()
    goal_list = pygame.sprite.Group()
    player_list = pygame.sprite.Group()

    # Creates 10 enemies that will be displayed at random in the map.
    enemy_1 = Enemy()
    enemy_1.rect.x = random.randrange(0, 1500)
    enemy_1.rect.y = random.randrange(0, 2000)
    enemy_list.add(enemy_1)
    all_sprites_list.add(enemy_1)

    enemy_2 = Enemy()
    enemy_2.rect.x = random.randrange(0, 1500)
    enemy_2.rect.y = random.randrange(0, 2000)
    enemy_list.add(enemy_2)
    all_sprites_list.add(enemy_2)

    enemy_3 = Enemy()
    enemy_3.rect.x = random.randrange(0, 1500)
    enemy_3.rect.y = random.randrange(0, 2000)
    enemy_list.add(enemy_3)
    all_sprites_list.add(enemy_3)

    enemy_4 = Enemy()
    enemy_4.rect.x = random.randrange(0, 1500)
    enemy_4.rect.y = random.randrange(0, 2000)
    enemy_list.add(enemy_4)
    all_sprites_list.add(enemy_4)

    enemy_5 = Enemy()
    enemy_5.rect.x = random.randrange(0, 1500)
    enemy_5.rect.y = random.randrange(0, 2000)
    enemy_list.add(enemy_5)
    all_sprites_list.add(enemy_5)

    enemy_6 = Enemy()
    enemy_6.rect.x = random.randrange(0, 1500)
    enemy_6.rect.y = random.randrange(0, 2000)
    enemy_list.add(enemy_6)
    all_sprites_list.add(enemy_6)

    enemy_7 = Enemy()
    enemy_7.rect.x = random.randrange(0, 1500)
    enemy_7.rect.y = random.randrange(0, 2000)
    enemy_list.add(enemy_7)
    all_sprites_list.add(enemy_7)

    enemy_8 = Enemy()
    enemy_8.rect.x = random.randrange(0, 1500)
    enemy_8.rect.y = random.randrange(0, 2000)
    enemy_list.add(enemy_8)
    all_sprites_list.add(enemy_8)

    enemy_9 = Enemy()
    enemy_9.rect.x = random.randrange(0, 1500)
    enemy_9.rect.y = random.randrange(0, 2000)
    enemy_list.add(enemy_9)
    all_sprites_list.add(enemy_9)

    enemy_10 = Enemy()
    enemy_10.rect.x = random.randrange(0, 1500)
    enemy_10.rect.y = random.randrange(0, 2000)
    enemy_list.add(enemy_10)
    all_sprites_list.add(enemy_10)

    # Creates 10 crates that will be displayed at random in the map.
    crate_1 = Crate()
    crate_1.rect.x = random.randrange(0, 1500)
    crate_1.rect.y = random.randrange(0, 2000)
    crate_list.add(crate_1)
    all_sprites_list.add(crate_1)

    crate_2 = Crate()
    crate_2.rect.x = random.randrange(0, 1500)
    crate_2.rect.y = random.randrange(0, 2000)
    crate_list.add(crate_2)
    all_sprites_list.add(crate_2)

    crate_3 = Crate()
    crate_3.rect.x = random.randrange(0, 1500)
    crate_3.rect.y = random.randrange(0, 2000)
    crate_list.add(crate_3)
    all_sprites_list.add(crate_3)

    crate_4 = Crate()
    crate_4.rect.x = random.randrange(0, 1500)
    crate_4.rect.y = random.randrange(0, 2000)
    crate_list.add(crate_4)
    all_sprites_list.add(crate_4)

    crate_5 = Crate()
    crate_5.rect.x = random.randrange(0, 1500)
    crate_5.rect.y = random.randrange(0, 2000)
    crate_list.add(crate_5)
    all_sprites_list.add(crate_5)

    crate_6 = Crate()
    crate_6.rect.x = random.randrange(0, 1500)
    crate_6.rect.y = random.randrange(0, 2000)
    crate_list.add(crate_6)
    all_sprites_list.add(crate_6)

    crate_7 = Crate()
    crate_7.rect.x = random.randrange(0, 1500)
    crate_7.rect.y = random.randrange(0, 2000)
    crate_list.add(crate_7)
    all_sprites_list.add(crate_7)

    crate_8 = Crate()
    crate_8.rect.x = random.randrange(0, 1500)
    crate_8.rect.y = random.randrange(0, 2000)
    crate_list.add(crate_8)
    all_sprites_list.add(crate_8)

    crate_9 = Crate()
    crate_9.rect.x = random.randrange(0, 1500)
    crate_9.rect.y = random.randrange(0, 2000)
    crate_list.add(crate_9)
    all_sprites_list.add(crate_9)

    crate_10 = Crate()
    crate_10.rect.x = random.randrange(0, 1500)
    crate_10.rect.y = random.randrange(0, 2000)
    crate_list.add(crate_10)
    all_sprites_list.add(crate_10)

    # Creates the goal for the game.
    goal_obj = Goal()
    goal_obj.rect.x = 800
    goal_obj.rect.y = 800
    goal_list.add(goal_obj)
    all_sprites_list.add(goal_obj)

    # Creates the player's collision.
    player_obj = Player()
    player_obj.rect.x = player_x
    player_obj.rect.y = player_y
    player_list.add(player_obj)
    all_sprites_list.add(player_list)


    while True:
        # THe main game loop.
        display_surface.blit(background_game, (background_x, background_y))
        game_interface.score_board()
        goal_conductor.play()
        goal_animations['goal'].blit(display_surface, (goal_obj.rect.x, goal_obj.rect.y))

        for event in pygame.event.get():

            # Will handle exiting the program.
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # Restarts the game if the player press the Enter key.
                elif event.key == K_RETURN:
                    main()

                elif event.key == K_UP:
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
                    gunshot.play()
                    if direction == up:
                        bullet = upBullet()
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
                player_obj.rect.y -= rate
                if move_background:
                    background_y += rate
                    goal_obj.rect.y += rate
                    enemy_1.rect.y += rate
                    enemy_2.rect.y += rate
                    enemy_3.rect.y += rate
                    enemy_4.rect.y += rate
                    enemy_5.rect.y += rate
                    enemy_6.rect.y += rate
                    enemy_7.rect.y += rate
                    enemy_8.rect.y += rate
                    enemy_9.rect.y += rate
                    enemy_10.rect.y += rate

                    crate_1.rect.y += rate
                    crate_2.rect.y += rate
                    crate_3.rect.y += rate
                    crate_4.rect.y += rate
                    crate_5.rect.y += rate
                    crate_6.rect.y += rate
                    crate_7.rect.y += rate
                    crate_8.rect.y += rate
                    crate_9.rect.y += rate
                    crate_10.rect.y += rate
            if move_down:
                player_y += rate
                player_obj.rect.y += rate
                if move_background:
                    background_y -= rate
                    goal_obj.rect.y -= rate
                    enemy_1.rect.y -= rate
                    enemy_2.rect.y -= rate
                    enemy_3.rect.y -= rate
                    enemy_4.rect.y -= rate
                    enemy_5.rect.y -= rate
                    enemy_6.rect.y -= rate
                    enemy_7.rect.y -= rate
                    enemy_8.rect.y -= rate
                    enemy_9.rect.y -= rate
                    enemy_10.rect.y -= rate

                    crate_1.rect.y -= rate
                    crate_2.rect.y -= rate
                    crate_3.rect.y -= rate
                    crate_4.rect.y -= rate
                    crate_5.rect.y -= rate
                    crate_6.rect.y -= rate
                    crate_7.rect.y -= rate
                    crate_8.rect.y -= rate
                    crate_9.rect.y -= rate
                    crate_10.rect.y -= rate
            if move_left:
                player_x -= rate
                player_obj.rect.x -= rate
                if move_background:
                    background_x += rate
                    goal_obj.rect.x += rate
                    enemy_1.rect.x += rate
                    enemy_2.rect.x += rate
                    enemy_3.rect.x += rate
                    enemy_4.rect.x += rate
                    enemy_5.rect.x += rate
                    enemy_6.rect.x += rate
                    enemy_7.rect.x += rate
                    enemy_8.rect.x += rate
                    enemy_9.rect.x += rate
                    enemy_10.rect.x += rate

                    crate_1.rect.x += rate
                    crate_2.rect.x += rate
                    crate_3.rect.x += rate
                    crate_4.rect.x += rate
                    crate_5.rect.x += rate
                    crate_6.rect.x += rate
                    crate_7.rect.x += rate
                    crate_8.rect.x += rate
                    crate_9.rect.x += rate
                    crate_10.rect.x += rate
            if move_right:
                player_x += rate
                player_obj.rect.x += rate
                if move_background:
                    background_x -= rate
                    goal_obj.rect.x -= rate
                    enemy_1.rect.x -= rate
                    enemy_2.rect.x -= rate
                    enemy_3.rect.x -= rate
                    enemy_4.rect.x -= rate
                    enemy_5.rect.x -= rate
                    enemy_6.rect.x -= rate
                    enemy_7.rect.x -= rate
                    enemy_8.rect.x -= rate
                    enemy_9.rect.x -= rate
                    enemy_10.rect.x -= rate

                    crate_1.rect.x -= rate
                    crate_2.rect.x -= rate
                    crate_3.rect.x -= rate
                    crate_4.rect.x -= rate
                    crate_5.rect.x -= rate
                    crate_6.rect.x -= rate
                    crate_7.rect.x -= rate
                    crate_8.rect.x -= rate
                    crate_9.rect.x -= rate
                    crate_10.rect.x -= rate
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
        if player_x > screen_width - (screen_width // 3):
            if background_x > - screen_width:
                player_x = screen_width - (screen_width // 3)
                player_obj.rect.x = screen_width - (screen_width // 3)
                move_background = True
            elif background_x <= - screen_width:
                background_x = - screen_width
                if player_x > screen_width - player_width:
                    player_x = screen_width - player_width
                    player_obj.rect.x = screen_width - player_width
        elif player_x < screen_width//4:
            if background_x < - player_obj.rect.x:
                player_x = screen_width//4
                move_background = True
            elif background_x < - player_obj.rect.x:
                background_x = player_obj.rect.x
                if player_x < 0:
                    player_x = 0
                    player_obj.rect.x = 0

        else:
            move_background = False

        if player_y < 0:
            player_y = 0
            player_obj.rect.y = 0
        if player_y > screen_height - screen_height // 3:
            if background_y > - screen_height:
                player_y = screen_height - screen_height // 3
                player_obj.rect.y = screen_height - screen_height // 3
                move_background = True
            elif background_y <= - screen_height:
                background_y = - screen_height
                if player_y > screen_height - player_height:
                    player_y = screen_height - player_height
                    player_obj.rect.y = screen_height - player_height
        if player_y < screen_height // 4:
            if background_y > - screen_height:
                player_y = screen_height // 4
                player_obj.rect.y = screen_height // 4
                move_background = True
            elif background_y <= - screen_height:
                background_y = - screen_height

        all_sprites_list.update()

        for bullet in bullet_list:
            # See if it hit an enemy
            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemy_list, True)
            crate_hit_list = pygame.sprite.spritecollide(bullet, crate_list, True)

            # For each enemy hit, remove the bullet
            for enemy in enemy_hit_list:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
                game_interface.score += 10
                deathsound.play()

            for crate in crate_hit_list:
                breaksound.play()
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)
                game_interface.score += 5

            # Remove the bullet if it flies out of the screen
            if bullet.rect.y < -10 or bullet.rect.y > 500 or bullet.rect.x < -10 or bullet.rect.x > 650:
                print('off screen')
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)

        for player in player_list:
            player_hit_list = pygame.sprite.spritecollide(player_obj, goal_list, True)

            for i in player_hit_list:
                end()

        all_sprites_list.draw(display_surface)
        pygame.display.update()
        clock.tick(30)

def main():
    """This function runs the main menu for the game."""
    game_interface.all_buttons_inactive()
    game_interface.score = 0
    pygame.mixer.music.stop()

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