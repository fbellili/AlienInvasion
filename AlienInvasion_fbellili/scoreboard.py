"""
Program: Scoreboard Class
Author: Farouk Bellili
Purpose: Render and display the Heads-Up Display (HUD) for the alien invasion.
Starter Code: chapter 14.
Date: 2026-04-28
"""

import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """
    A class to report scoring and game-state information on the HUD.

    Displays four pieces of information:
    - Current score (top-right)
    - High score (top-center)
    - Current level (below current score)
    - Remaining lives as ship icons (top-left, below the ship's travel area)
    """

    def __init__(self, ai_game):
        """
        Initialize scorekeeping attributes and prepare all HUD images.

        Args:
            ai_game (AlienInvasion): The main game instance, providing access
                                     to the screen, settings, and stats.
        """
        # Store the game instance so prep_ships() can create Ship objects.
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings shared by all HUD text elements.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare all four HUD elements at startup.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()


    def prep_score(self):
        """
        Turn the current score into a rendered image positioned top-right.

        Rounds the score to the nearest 10 and formats it with comma
        separators for readability (e.g., 1,050 instead of 1050).
        """
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color
        )

        # Align the score to the top-right corner with a small margin.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """
        Turn the high score into a rendered image centered at the top.

        The high score is also rounded and comma-formatted, then placed
        at the same vertical level as the current score.
        """
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.bg_color
        )

        # Center the high score horizontally at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """
        Turn the current level into a rendered image below the score.

        Positioned 10 pixels below the bottom of the score image so it
        stays readable without overlapping the score.
        """
        level_str = str(self.stats.level)
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color
        )

        # Place the level just below the current score, right-aligned.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """
        Build a group of ship icons representing the player's remaining lives.

        Creates one Ship sprite per life and lines them up horizontally
        starting from the top-left corner of the screen, below the HUD
        margin. Each icon is spaced by one ship-width so they don't overlap.
        """
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)


    def check_high_score(self):
        """
        Compare the current score to the high score and update if needed.

        If the player has beaten the high score, the high score attribute
        and its rendered image are both updated immediately.
        """
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """
        Draw all HUD elements to the screen each frame.

        Renders the current score, high score, level, and life icons so
        the player always has up-to-date game-state information.
        """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
