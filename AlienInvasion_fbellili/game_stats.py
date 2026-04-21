"""
Program: Game Stats
Author: Farouk Bellili
Purpose: Track runtime statistics for the Alien Invasion game, including
         the number of ships (lives) remaining and whether the game is active.
Starter Code: chapter 13.
Date: 2026-04-14
"""


class GameStats:
    """
    Track statistics for the Alien Invasion game.

    Maintains the number of ships remaining and the active/inactive
    game state used to pause the game on a loss condition.
    """

    def __init__(self, ai_game):
        """
        Initialize statistics.

        Args:
            ai_game (AlienInvasion): The main game instance, used to access
                                     the settings for ship limit.
        """
        self.settings = ai_game.settings
        self.reset_stats()

        # Game starts in an inactive state until the player is ready.
        self.game_active = True

    def reset_stats(self):
        """
        Initialize statistics that can change during the game.

        Called at startup and again each time a new game begins so
        the ship count is restored to its maximum.
        """
        self.ships_left = self.settings.ship_limit
