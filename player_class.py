# This will be the player class file.
import pygame
from pygame.locals import *


class Player:
    """Class that creates and defines the player."""

    def __init__(self, health, attack, defense, weapon, movement_speed, position, surface):
        # Define and assign some self values.
        self.health = health
        self.attack = attack
        self.defense = defense
        self.weapon = weapon
        self.movement_speed = movement_speed
        self.position = position
        self.surface = surface
        self.character_surface = pygame.Surface((1, 1), flags=SRCALPHA, depth=32)
        self.character_surface.fill((0, 0, 0, 0))

    def update_health(self, health_change):
        """This function will allow us to raise or lower the player's current health."""
        self.health += health_change
        return self.health

    def update_attack(self, attack_change):
        """This function will allow us to raise or lower the player's attack damage."""
        self.attack += attack_change
        return self.attack

    def update_defense(self, defense_change):
        """This function will allow us to raise or lower the player's defense."""
        self.defense += defense_change
        return self.defense

    def update_weapon(self, weapon_type):
        """This function will allow us to change the weapon the player has."""
        self.weapon = weapon_type
        return self.weapon

    def update_speed(self, speed_change):
        """This function will allow us to change the movement speed of the player."""
        self.movement_speed = speed_change
        return self.movement_speed

    def update_position(self, position_change):
        """This function will allow us to change the position of the player."""
        self.position = position_change
        return self.position

    def display_player(self):
        """This function will display the player."""
        self.character_surface.blit(self.character_surface, self.position)