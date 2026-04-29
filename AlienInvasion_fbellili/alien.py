"""
Program: Alien Class
Author: Farouk Bellili
Purpose: Manage a single alien in the fleet. Aliens spawn on the right side
         of the screen and travel horizontally to the left toward the ship.
Starter Code: chapter 14.
Date: 2026-04-28
"""

import pygame
from pygame.sprite import Sprite
from pathlib import Path


class Alien(Sprite):
    """
    A class to represent a single alien in the fleet.

    Aliens move horizontally (left) and shift vertically when they
    reach the top or bottom boundary of the screen.
    """

    def __init__(self, ai_game):
        """
        Initialize the alien and set its starting position.

        Args:
            ai_game (AlienInvasion): The main game instance, used to access
                                     the screen and settings.
        """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load alien image using pathlib for cross-platform compatibility.
        image_path = Path("images") / "alien.bmp"
        self.image = pygame.image.load(str(image_path))
        self.rect = self.image.get_rect()

        # Starting position is set by _create_alien() in AlienInvasion.
        # Default to top-right area until placed by the fleet builder.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store a float for precise horizontal positioning.
        self.x = float(self.rect.x)

    def check_edges(self):
        """
        Return True if the alien has reached the top or bottom screen edge.

        Used to determine when the fleet should drop and reverse vertical
        direction so it continues to fill the visible play area.

        Returns:
            bool: True if the alien is at or beyond a vertical screen edge.
        """
        screen_rect = self.screen.get_rect()
        return self.rect.bottom >= screen_rect.bottom or self.rect.top <= 0

    def update(self):
        """
        Move the alien horizontally to the left on each frame.

        The horizontal speed is read from settings so it can be adjusted
        for difficulty scaling in future milestones.
        """
        self.x -= self.settings.alien_speed
        self.rect.x = self.x
