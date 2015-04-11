import pygame
from pygame.locals import *
import sys
import button_class

pygame.init()

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)


class MenuItem(pygame.font.Font):
    """Class that creates a menu item."""
    def __init__(self, text, pos=(0, 0), font=None, font_size=30,
                 font_color=white):
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
        self.is_selected = False

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
    def __init__(self, screen, items, bg_color=black, font=None, fon_size=30, font_color=white):

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

        self.mouse_is_visible = True
        self.cur_item = None

    def set_mouse_visibility(self):
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

    def set_item_selection(self, key):
        for item in self.items:
            # Return all to neutral.
            item.set_italic(False)
            item.set_font_color(white)

        if self.cur_item is None:
            self.cur_item = 0
        else:
            # Find the chose item
            if key == pygame.K_UP and self.cur_item > 0:
                self.cur_item -= 1
            elif key == pygame.K_UP and self.cur_item == 0:
                self.cur_item = len(self.items) - 1
            elif key == pygame.K_DOWN and self.cur_item < len(self.items) - 1:
                self.cur_item += 1
            elif key == pygame.K_DOWN and self.cur_item == len(self.items) - 1:
                self.cur_item = 0

        self.items[self.cur_item].set_italic(True)
        self.items[self.cur_item].set_font_color(red)

    def set_mouse_selection(self, item, mpos):
        """Marks the MenuItem the mouse cursor hovers on."""
        if item.is_mouse_selection(mpos):
            item.set_font_color(red)
            item.set_italic(True)
        else:
            item.set_font_color(white)
            item.set_italic(False)

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
                    else:
                        self.mouse_is_visible = False
                        self.set_item_selection(event.key)

            if pygame.mouse.get_rel() != (0, 0):
                self.mouse_is_visible = True
                self.cur_item = None

            self.set_mouse_visibility()

            # Redraw the background.
            self.screen.fill(self.bg_color)

            for item in self.items:
                if self.mouse_is_visible:
                    mpos = pygame.mouse.get_pos()
                    self.set_mouse_selection(item, mpos)
                self.screen.blit(item.label, item.position)

            pygame.display.flip()

if __name__ == "__main__":
    # Creating the screen
    screen = pygame.display.set_mode((640, 480), 0, 32)

    menu_items = ('Start', 'Setting', 'Quit')

    pygame.display.set_caption('Game Menu')
    gm = GameMenu(screen, menu_items)
    gm.run()