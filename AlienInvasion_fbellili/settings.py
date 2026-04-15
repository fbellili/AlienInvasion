"""
Program: Alien Invasion Settings
Author: Farouk Bellili
Purpose: Store all game settings.
Starter Code: Based on classroom tutorial.
Date: 2026-04-14
"""

class Settings:
    """A class to store settings."""

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        self.ship_speed = 1.5

        self.bullet_speed = 3.0
        self.bullet_width = 10
        self.bullet_height = 4
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3