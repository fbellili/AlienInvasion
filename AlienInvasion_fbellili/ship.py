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
    """A class to manage the ship."""

    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        image_path = Path("images") / "ship.bmp"
        self.image = pygame.image.load(str(image_path))
        self.rect = self.image.get_rect()

        # LEFT side position
        self.rect.midleft = self.screen_rect.midleft

        self.y = float(self.rect.y)

        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        self.rect.y = self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)
