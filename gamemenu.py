import pygame
from pygame.locals import *
import sys
import button_class

pygame.init()


class GameMenu():
    def __init__(self, screen, items, bg_color=(0,0,0), font=None, fon_size=30, font_color=(255,255,255)):

        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bg_color = bg_color
        self.clock = pygame.time.Clock()

        self.items = items
        self.font = pygame.font.SysFont(font, fon_size)
        self.font_color = font_color

        self.items = []
        for index, item in enumerate(items):
            label = self.font.render(item, 1, font_color)

            width = label.get_rect().width
            height = label.get_rect().height

            position_x = (self.scr_width/2) - (width/2)
            # t_h: total height of text block
            t_h = len(items) * height
            position_y = (self.scr_height/2) - (t_h/2) + (index * height)

            self.items.append([item, label, (width, height), (position_x, position_y)])

    def run(self):
        while True:
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            self.screen.fill(self.bg_color)

            for name, label, (width, height), (position_x, position_y) in self.items:
                self.screen.blit(label, (position_x, position_y))

            pygame.display.flip()

if __name__ == "__main__":
    screen = pygame.display.set_mode((640, 480), 0, 32)

    menu_items = ('Start', 'Quit')

    pygame.display.set_caption('Game Menu')
    gm = GameMenu(screen, menu_items)
    gm.run()