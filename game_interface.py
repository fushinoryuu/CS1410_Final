import pygame
from pygame.locals import *
from button_class import SimpleButton

pygame.init()

class GameInterface:
    def __init__(self):
        self.display_width = 640
        self.display_height = 480
        self.status = 0

        self.background_mainmenu = pygame.image.load('gameimages\mainmenu.png')
        self.background_credits = pygame.image.load('gameimages\credits.png')

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

        button_width = self.display_width//5
        button_height = button_width//4
        button_x = self.display_width//2 - button_width//2
        button_y = self.display_height//2 - button_height//2 + 30
        button_position = (button_x, button_y)

        self.start_button = SimpleButton(button_width, button_height, self.orange, self.grey, "Start Game",
                                         self.display_surface, button_position)
        self.quit_button = SimpleButton(button_width, button_height, self.orange, self.grey, "Quit Game",
                                         self.display_surface, (button_x + 160, button_y))
        self.credits_button = SimpleButton(button_width, button_height, self.orange, self.grey, "Credits",
                                         self.display_surface, (button_x - 160, button_y))
        self.button_list = [self.start_button, self.quit_button, self.credits_button]

        self.game_font = pygame.font.SysFont("Arial", 100)

        self.score_active = False

    def all_buttons_inactive(self):
        for i in self.button_list:
            i.inactive()

    def all_buttons_active(self):
        for i in self.button_list:
            i.activate()

    def start_setup (self):
        self.all_buttons_inactive()

    def display_all_buttons(self):
        for x in self.button_list:
            if x.active:
                x.display_button()
                x.display_highlighted()

    def display_interface(self):
        if self.status == 0:
            self.display_surface.blit(self.background_mainmenu, (0, 0))
            self.display_all_buttons()
        elif self.status == 1:
            self.display_surface.blit(self.background_credits, (0, 0))
            self.display_all_buttons()

    def reset_game(self):
        self.start_setup()
        self.display_interface()