"""
Program: Game Stats
Author: Farouk Bellili
Purpose: Track runtime statistics for the Alien Invasion game, including
         ships remaining, current score, high score, and level. The high
         score persists across games; all other stats reset each new game.
Starter Code: chapter 14.
Date: 2026-04-28
"""


class GameStats:
    """
    Track statistics for the Alien Invasion game.

    Separates stats that reset each game (ships, score, level) from the
    high score, which persists for the entire session.
    """

    def __init__(self, ai_game):
        """
        Initialize statistics.

        Args:
            ai_game (AlienInvasion): The main game instance, used to access
                                     settings for the ship limit.
        """
        self.settings = ai_game.settings
        self.reset_stats()

        # High score never resets during a session.
        self.high_score = 0

        # Game starts inactive — player must click Play to begin.
        self.game_active = False

    def reset_stats(self):
        """
        Initialize statistics that change during the game.

        Resets ships remaining, score, and level back to their starting
        values. Called at startup and at the beginning of each new game.
        """
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
