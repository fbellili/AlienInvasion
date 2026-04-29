"""
Program: Ship Class
Author: Farouk Bellili
Purpose: Manage the player ship positioned on the left edge of the screen,
         moving vertically (up/down) and firing bullets horizontally to the
         right. Inherits from Sprite so it can be used in the lives HUD.
Starter Code: chapter 14.
Date: 2026-04-28
"""

import pygame
from pygame.sprite import Sprite
from pathlib import Path


class Ship(Sprite):
    """
    A class to manage the player's ship.

    The ship is anchored to the left edge of the screen and moves
    vertically. It inherits from Sprite so Scoreboard can draw ship
    icons in the HUD to represent remaining lives.
    """

    def __init__(self, ai_game):
        """
        Initialize the ship and set its starting position.

        Args:
            ai_game (AlienInvasion): The main game instance, used to access
                                     the screen and settings.
        """
        super().__init__()
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
        Update the ship's vertical position based on movement flags.

        Clamps movement so the ship cannot travel beyond the top or
        bottom screen edges.
        """
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        self.rect.y = self.y

    def center_ship(self):
        """
        Re-center the ship on the left edge after a life is lost.

        Resets the vertical position to the middle of the screen and
        clears movement flags so no unintended drift occurs.
        """
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)
        self.moving_up = False
        self.moving_down = False

    def blitme(self):
        """Draw the ship at its current location on the screen."""
        self.screen.blit(self.image, self.rect)
