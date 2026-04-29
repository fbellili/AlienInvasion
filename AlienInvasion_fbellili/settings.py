"""
Program: Alien Invasion Settings
Author: Farouk Bellili
Purpose: Store all static and dynamic game settings for the side-scrolling
         Alien Invasion game. Dynamic settings reset each new game and scale
         up as the player levels up.
Starter Code: chapter 14.
Date: 2026-04-28
"""


class Settings:
    """
    A class to store all settings for the Alien Invasion game.

    Static settings (screen size, bullet limits, etc.) are set once in
    __init__(). Dynamic settings (speeds, alien points) live in
    initialize_dynamic_settings() so they reset cleanly on each new game.
    """

    def __init__(self):
        """
        Initialize the game's static settings and call the dynamic setup.

        Static settings never change mid-game. Dynamic settings are
        initialized separately so they can be reset when a new game starts.
        """
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 10
        self.bullet_height = 4
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien fleet settings
        # Aliens bounce off top/bottom edges and shift left on each bounce.
        self.fleet_drop_speed = 5

        # Difficulty scaling — how fast the game speeds up each level.
        self.speedup_scale = 1.1
        # How quickly alien point values increase each level.
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """
        Initialize settings that change as the game progresses.

        Called at startup and again every time the player starts a new game
        so speeds and point values return to their baseline.
        fleet_direction: 1 = moving down, -1 = moving up.
        """
        self.ship_speed = 1.5
        self.bullet_speed = 6.0
        self.alien_speed = 0.5      # slower so the fleet is beatable
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """
        Scale up movement speeds and alien point value for the next level.

        Multiplies each speed by speedup_scale and raises alien_points by
        score_scale, keeping the increase as a whole integer.
        """
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
