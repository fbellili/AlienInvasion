"""
Program: Bullet Class
Author: Farouk Bellili
Purpose: Manage bullets fired horizontally to the right from the ship's nose,
         consistent with the side-scrolling game mechanics.
Starter Code: chapter 14.
Date: 2026-04-14
"""

import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """
    A class to manage bullets fired from the ship.

    Each bullet is a rectangle that travels horizontally from left to
    right across the screen, disappearing when it exits the right edge.
    """

    def __init__(self, ai_game):
        """
        Create a bullet object at the ship's current nose position.

        Args:
            ai_game (AlienInvasion): The main game instance, used to access
                                     the screen, settings, and ship position.
        """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect and position it at the ship's right side.
        self.rect = pygame.Rect(
            0, 0,
            self.settings.bullet_width,
            self.settings.bullet_height
        )
        self.rect.midleft = ai_game.ship.rect.midright

        # Store the bullet's position as a float for precision.
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet horizontally to the right on each frame."""
        self.x += self.settings.bullet_speed
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
