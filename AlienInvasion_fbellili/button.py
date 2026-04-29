"""
Program: Button Class
Author: Farouk Bellili
Purpose: Build a clickable Play button rendered as a filled rectangle with
         a centered text label. Used to start and restart the game without
         requiring a keyboard shortcut.
Starter Code: chapter 14.
Date: 2026-04-28
"""

import pygame.font


class Button:
    """
    A class to create a labeled button for the game UI.

    Renders a filled rectangle with centered text that can be drawn
    anywhere on the screen. Designed to be reusable for any button label.
    """

    def __init__(self, ai_game, msg):
        """
        Initialize button attributes and prepare the text image.

        Args:
            ai_game (AlienInvasion): The main game instance, used to access
                                     the screen for sizing and centering.
            msg (str): The text label to display on the button.
        """
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Button dimensions and colors.
        self.width, self.height = 200, 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button rect and center it on the screen.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Render the message image once — it doesn't change.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """
        Render the button label as an image and center it on the button.

        Args:
            msg (str): The text string to render onto the button surface.
        """
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color
        )
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """
        Draw the button rectangle and its text label to the screen.

        Fills the button area with button_color, then blits the text
        image on top so it appears centered inside the button.
        """
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
