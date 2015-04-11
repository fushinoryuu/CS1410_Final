import pygame
from pygame.locals import *
import sys

pygame.init()

# Rgb values
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)


class MenuItem(pygame.font.Font):
    """Class that creates a menu item."""
    def __init__(self, text, font=None, font_size=30, font_color=white, pos=(0, 0)):
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

    def is_mouse_selection(self, position):
        """Checks the position of the mouse to see if its over a menu item."""
        if(position[0] >= self.position_x and position[0] <= self.position[0] + self.width) and \
                (position[1] >= self.position_y and position[1] <= self.position_y + self.height):
            return True
        else:
            return False

    def set_position(self, x, y):
        """Sets the position of the menu item."""
        self.position = (x, y)
        self.position_x = x
        self.position_y = y

    def set_font_color(self, rgb):
        """Sets the font color."""
        self.font_color = rgb
        self.label = self.render(self.text, 1, self.font_color)


class GameMenu():
    """Class that creates a menu."""
    def __init__(self, screen, items, funcs, bg_color=black, font=None, font_size=30, font_color=white):

        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bg_color = bg_color
        self.clock = pygame.time.Clock()

        self.funcs = funcs
        self.items = []
        for index, item in enumerate(items):
            menu_item = MenuItem(item, font, font_size, font_color)

            # t_h: total height of text block
            t_h = len(items) * menu_item.height
            pos_x = (self.scr_width/2) - (menu_item.width/2)
            pos_y = (self.scr_height/2) - (t_h /2) + ((index * 2) + index * menu_item.height)

            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)

        self.mouse_is_visible = True
        self.cur_item = None

    def set_mouse_visibility(self):
        """Changes the visibility of the mouse cursor."""
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

    def set_keyboard_selection(self, key):
        """Marks the MenuItem chosen via up and down keys."""
        for item in self.items:
            # Return all to neutral.
            item.set_italic(False)
            item.set_font_color(white)

        if self.cur_item is None:
            self.cur_item = 0
        else:
            # Find the chosen item.
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

        # Finally check if Enter or Space is pressed
        if key == pygame.K_SPACE or key == pygame.K_RETURN:
            text = self.items[self.cur_item].text
            self.funcs[text]()

    def set_mouse_selection(self, item, mpos):
        """Marks the MenuItem the mouse cursor hovers on."""
        if item.is_mouse_selection(mpos):
            item.set_font_color(red)
            item.set_italic(True)
        else:
            item.set_font_color(white)
            item.set_italic(False)

    def run(self):
        """This is the main function that runs the loop for the menu."""
        while True:
            self.clock.tick(30)

            mpos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    self.mouse_is_visible = False
                    self.set_keyboard_selection(event.key)
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.items:
                        if item.is_mouse_selection(mpos):
                            self.funcs[item.text]()

            if pygame.mouse.get_rel() != (0, 0):
                self.mouse_is_visible = True
                self.cur_item = None

            self.set_mouse_visibility()

            # Redraw the background.
            self.screen.fill(self.bg_color)

            for item in self.items:
                if self.mouse_is_visible:
                    self.set_mouse_selection(item, mpos)
                self.screen.blit(item.label, item.position)

            pygame.display.flip()

if __name__ == "__main__":
    def hello_world():
        print("Hello World!")

    # Creating the screen
    screen = pygame.display.set_mode((640, 480), 0, 32)

    menu_items = ('Start', 'Quit')
    funcs = {'Start': hello_world, 'Quit': sys.exit}

    pygame.display.set_caption('Game Menu')
    gm = GameMenu(screen, funcs.keys(), funcs)
    gm.run()