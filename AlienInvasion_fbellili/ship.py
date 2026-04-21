"""
Program: Ship Class
Author: Farouk Bellili
Purpose: Manage the player ship with vertical movement.
Starter Code: chapter12.
Date: 2026-04-14
"""

import pygame
from pathlib import Path


class Ship:
    """
    A class to manage the player's ship.

    The ship is anchored to the left edge of the screen and moves
    vertically. It fires bullets horizontally toward incoming aliens.
    """

    def __init__(self, ai_game):
        """
        Initialize the ship and set its starting position.

        Args:
            ai_game (AlienInvasion): The main game instance, used to access
                                     the screen and settings.
        """
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load ship image using pathlib for cross-platform compatibility.
        image_path = Path("images") / "ship.bmp"
        self.image = pygame.image.load(str(image_path))
        self.rect = self.image.get_rect()

        # Position the ship on the left edge, vertically centered.
        self.rect.midleft = self.screen_rect.midleft

        # Store a float for precise vertical positioning.
        self.y = float(self.rect.y)

        # Movement flags.
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """
        Update the ship's position based on movement flags.

        Prevents the ship from moving beyond the top or bottom screen edges.
        """
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        self.rect.y = self.y

    def center_ship(self):
        """
        Re-center the ship on the left edge after a life is lost.

        Resets vertical position to the middle of the screen.
        """
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)

    def blitme(self):
        """Draw the ship at its current location on the screen."""
        self.screen.blit(self.image, self.rect)


    def blitme(self):
        self.screen.blit(self.image, self.rect)
