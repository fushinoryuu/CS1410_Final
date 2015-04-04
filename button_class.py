# Mark's buttonClass.py
import pygame
from pygame.locals import *


class SimpleButton:
    """class that creates button objects."""
    def __init__(self, width, height, color, text_color, label, surface, position):

        # Define and assign some self values.
        self.active = True
        self.label = label
        self.surface = surface
        self.position = position
        self.button_color = color
        self.text_color = text_color

        # Generate a greyed-out version of color and a highlighted version of color.
        self.button_greyed = (color[0] * .25, color[1] * .25, color[2] * .25)
        self.highlight_color = (color[0] + ((255 - color[0])//2),
                                color[1] + ((255 - color[1])//2),
                                color[2] + ((255 - color[2])//2))

        # Assign and calculates some size values.
        self.height = height
        self.width = width
        self.h_width = self.width//2
        self.radius = self.height//2
        self.t_height = int(self.height * .60)

        # Creates button surface
        self.button_surface = pygame.Surface((self.width, self.height), flags=SRCALPHA, depth=32)
        self.button_surface.fill((0, 0, 0, 0))

    def test(self):
        return 1

    def button_bg(self, color):
        """Helper Method to create button background"""

        # create square with rounded corners
        pygame.draw.circle(self.button_surface, color, (self.radius, self.radius),
                           self.radius)
        pygame.draw.circle(self.button_surface, color,
                           (self.width - self.radius, self.radius), self.radius)
        pygame.draw.rect(self.button_surface, color,
                         Rect((self.radius, 0), (self.width - 2 * self.radius,
                                                 self.height)))

    def button_text(self):
        """Helper function to make text surface and blit on button_surface."""

        # Set up the Font Object and how to Change Fonts
        button_font = pygame.font.SysFont("Sylfaen", self.t_height)
        
        # Render a Text Surface
        self.text_surface = button_font.render(self.label, True, self.text_color, None)
        w, h = self.text_surface.get_size()
        x_position = (self.width - w)//2
        y_position = (self.height - h)//2

        # Draw Text
        self.button_surface.blit(self.text_surface, (x_position, y_position))

    def clicked(self, mouse_xy):
        yes_or_no = False
        p1 = self.position
        p2 = (p1[0] + self.width, p1[1] + self.height)
        yes_or_no = (self.active and p1[0] <= mouse_xy[0] <= p2[0] and
                     p1[1] <= mouse_xy[1] <= p2[1])
        return yes_or_no

    def active(self):
        """Sets the button to active mode."""
        self.active = True

    def inactive(self):
        """Sets the button to inactive mode."""
        self.active = False

    def change_position(self, X, Y):
        """Allows the position of the button to be changed."""
        self.position = (X, Y)
        return self.position

    def display_highlighted(self):
        """Displays the highlighted version of the button."""
        self.button_bg(self.highlight_color)
        self.button_text()
        self.surface.blit(self.button_surface, self.position)

    def display_button(self):
        """Displays the button."""
        self.button_bg(self.button_color)
        self.button_text()
        self.surface.blit(self.button_surface, self.position)