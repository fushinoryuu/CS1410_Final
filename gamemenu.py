import pygame
from pygame.locals import *
import sys
import button_class

pygame.init()


class MenuItem(pygame.font.Font):
    """Class that creates a menu item."""
    def __init__(self, text, pos=(0,0), font=None, font_size=30,
                 font_color=(255,255,255)):
        pygame.font.Font.__init__(self,font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)
        self.position_x = pos[0]
        self.position_y = pos[1]
        self.position = pos

    def set_position(self, x, y):
        self.position = (x, y)
        self.position_x = x
        self.position_y = y

    def set_font_color(self, rgb):
        self.font_color = rgb
        self.label = self.render(self.text, 1, self.font_color)

    def is_mouse_selection(self, position):
        if (position[0] >= self.position_x and position[0] <= self.position[0] + self.width) and\
                (position[1] >= self.position_y and position[1] <= self.position_y + self.height):
            return True
        else:
            return False


class GameMenu():
    """Class that creates a menu."""
    def __init__(self, screen, items, bg_color=(0, 0, 0), font=None, fon_size=30, font_color=(255, 255, 255)):

        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bg_color = bg_color
        self.clock = pygame.time.Clock()

        self.items = []
        for index, item in enumerate(items):
            menu_item = MenuItem(item)

            # t_h: total height of text block
            t_h = len(items) * menu_item.height
            pos_x = (self.scr_width/2) - (menu_item.width/2)
            pos_y = (self.scr_height/2) - (t_h /2) + ((index * 2) + index * menu_item.height)

            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

    def run(self):
        while True:
            self.clock.tick(30)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            # Redraw the background.
            self.screen.fill(self.bg_color)

            for item in self.items:
                if item.is_mouse_selection(pygame.mouse.get_pos()):
                    item.set_font_color((255,0,0))
                    item.set_italic(True)
                else:
                    item.set_font_color((255, 255, 255))
                    item.set_italic(False)
                self.screen.blit(item.label, item.position)

            pygame.display.flip()

if __name__ == "__main__":
    # Creating the screen
    screen = pygame.display.set_mode((640, 480), 0, 32)

    menu_items = ('Start', 'Quit')

    pygame.display.set_caption('Game Menu')
    gm = GameMenu(screen, menu_items)
    gm.run()