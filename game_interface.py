import pygame
from pygame.locals import *
from button_class import SimpleButton

pygame.init()


class GameInterface:
    """This class represent the interface for the game's menu."""
    def __init__(self):
        self.display_width = 640
        self.display_height = 480
        self.status = 0

        # Load background images for the: main menu, credits, and end screen.
        self.background_mainmenu = pygame.image.load('gameimages/newmainmenuBG.png')
        self.background_credits = pygame.image.load('gameimages/credits.png')
        self.background_end = pygame.image.load('gameimages/end_background.png')

        self.display_surface = pygame.display.set_mode((self.display_width, self.display_height), 0, 32)
        pygame.display.set_caption('Commando Game')

        #RGB colors for later use
        self.rust = (151, 47, 0)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.dark_turquoise = (0, 64, 51)
        self.lite_turquoise = (0, 164, 151)
        self.orange = (176, 67, 17)
        self.grey = (50, 50, 50)
        self.yellow = (192, 150, 24)
        self.background_color = (0, 147, 134)

        self.button_width = self.display_width//5
        self.button_height = self.button_width//4
        self.button_x = self.display_width//2 - self.button_width//2
        self.button_y = self.display_height//2 - self.button_height//2 + 150
        self.button_position = (self.button_x, self.button_y)

        # Create 3 buttons that will be used in the game.
        self.start_button = SimpleButton(self.button_width, self.button_height, self.orange, self.grey, "Start Game",
                                         self.display_surface, self.button_position)
        self.quit_button = SimpleButton(self.button_width, self.button_height, self.orange, self.grey, "Quit Game",
                                         self.display_surface, (self.button_x + 160, self.button_y))
        self.credits_button = SimpleButton(self.button_width, self.button_height, self.orange, self.grey, "Credits",
                                         self.display_surface, (self.button_x - 160, self.button_y))
        self.button_list = [self.start_button, self.quit_button, self.credits_button]

        self.game_font = pygame.font.SysFont("Arial", 100)

        self.score = 0

    def all_buttons_inactive(self):
        """Makes all the buttons inactive."""
        for i in self.button_list:
            i.inactive()

    def all_buttons_active(self):
        """Makes all the buttons active."""
        for i in self.button_list:
            i.activate()

    def display_all_buttons(self):
        """Displays all the buttons that are active."""
        for x in self.button_list:
            if x.active:
                x.display_button()
                x.display_highlighted()

    def display_interface(self):
        """This function displays the buttons and the correct background."""
        self.start_button.change_position(self.button_position[0], self.button_position[1])
        self.credits_button.change_position(self.button_x - 160, self.button_y)
        self.quit_button.change_position(self.button_x + 160, self.button_y)
        if self.status == 0:
            self.display_surface.blit(self.background_mainmenu, (0, 0))
            self.display_all_buttons()
        elif self.status == 1:
            self.display_surface.blit(self.background_credits, (0, 0))
            self.display_all_buttons()

    def reset_game(self):
        """This function resets the game."""
        self.all_buttons_inactive()
        self.display_interface()

    def display_score(self, ypos):
        """A function that displays the score on the window."""
        score_string = "Player's Points: " + str(self.score)
        score_surface = self.game_font.render(score_string, True, self.white, None)
        score_surface = pygame.transform.scale(score_surface, (self.display_width - (self.display_width//3),
                                                                 self.display_height//10))
        w, h = score_surface.get_size()
        score_x = (self.display_width - w)//2
        score_y = ypos
        self.display_surface.blit(score_surface, (score_x, score_y))

    def score_board(self):
        """Tells the score where to be displayed."""
        self.all_buttons_inactive()
        self.display_score(0)

    def final(self):
        """Function that displays the ending screen when the player reaches the goal in the game."""
        self.display_surface.blit(self.background_end, (0, 0))
        self.display_score(250)
        self.all_buttons_inactive()
        self.start_button.active = True
        self.quit_button.active = True
        self.start_button.change_position(self.display_width//2 - 200, self.display_height//2 + 100)
        self.quit_button.change_position(self.display_width//2 + 100, self.display_height//2 + 100)
        self.display_all_buttons()