"""
Program: Alien Invasion Game
Author: Farouk Bellili
Purpose: Alien Invasion with vertical ship movement and horizontal shooting.
Starter Code: chapter12.
Date: 2026-04-14
"""

import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats


class AlienInvasion:
    """
    Overall class to manage game assets and behavior.

    Handles the main game loop, event processing, fleet creation and
    movement, collision detection, and loss/reset conditions for the
    side-scrolling variant of Alien Invasion.
    """

    def __init__(self):
        """
        Initialize the game, create screen and core objects.

        Sets up pygame, the display window, settings, statistics, the
        player ship, the bullet group, and the initial alien fleet.
        """
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """
        Start the main game loop.

        Continuously checks for events, updates all game objects,
        and redraws the screen at 60 frames per second.
        """
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    # ------------------------------------------------------------------ #
    # Event handling                                                       #
    # ------------------------------------------------------------------ #

    def _check_events(self):
        """
        Respond to keypresses and window events.

        Delegates keydown and keyup events to their respective helpers.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """
        Respond to keypresses.

        Args:
            event (pygame.event.Event): The keydown event to process.
        """
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """
        Respond to key releases.

        Args:
            event (pygame.event.Event): The keyup event to process.
        """
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    # ------------------------------------------------------------------ #
    # Bullet management                                                    #
    # ------------------------------------------------------------------ #

    def _fire_bullet(self):
        """
        Create a new bullet and add it to the bullets group.

        Respects the maximum number of bullets allowed on screen at once
        as defined in settings.
        """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """
        Update bullet positions and remove off-screen bullets.

        After moving all bullets to the right, any bullet whose left edge
        has passed the right side of the screen is removed. Then
        bullet-alien collisions are checked.
        """
        self.bullets.update()

        # Remove bullets that have left the right edge of the screen.
        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """
        Detect bullet-alien collisions and respond.

        Any bullet that overlaps an alien removes both objects. If the
        entire fleet is destroyed, the bullets are cleared and a new fleet
        is created.
        """
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if not self.aliens:
            # All aliens destroyed — clear remaining bullets and spawn new fleet.
            self.bullets.empty()
            self._create_fleet()

    # ------------------------------------------------------------------ #
    # Alien fleet management                                               #
    # ------------------------------------------------------------------ #

    def _create_fleet(self):
        """
        Create a full fleet of aliens on the right side of the screen.

        Aliens are arranged in a grid of columns and rows. The number of
        columns and rows is calculated to fit the screen with one alien's
        worth of margin on all sides. The fleet spawns off-screen to the
        right so it scrolls into view naturally.
        """
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height

        # Calculate how many columns and rows fit on screen.
        available_x = self.settings.screen_width - 2 * alien_width
        number_cols = available_x // (2 * alien_width)

        available_y = self.settings.screen_height - 3 * alien_height
        number_rows = available_y // (2 * alien_height)

        for col_number in range(number_cols):
            for row_number in range(number_rows):
                self._create_alien(col_number, row_number)

    def _create_alien(self, col_number, row_number):
        """
        Create an alien and place it in the fleet grid.

        Aliens are positioned starting from the right side of the screen.
        Column 0 is closest to the right edge; higher column numbers are
        further right (off-screen or near the edge), so the fleet enters
        from the right.

        Args:
            col_number (int): The column index (0 = rightmost visible column).
            row_number (int): The row index (0 = top row).
        """
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height

        # Place the alien: columns grow toward the right edge of the screen.
        alien.x = (
            self.settings.screen_width
            - alien_width
            - 2 * alien_width * col_number
        )
        alien.rect.x = alien.x

        # Rows are spaced from the top down.
        alien.rect.y = alien_height + 2 * alien_height * row_number

        self.aliens.add(alien)

    def _update_aliens(self):
        """
        Update positions of all aliens in the fleet.

        Checks whether any alien has reached a vertical screen edge; if so,
        the entire fleet drops and reverses vertical direction. Then checks
        whether any alien has collided with the ship or reached the left edge
        (behind the ship), triggering a ship hit.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Check for alien-ship collision.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Check for aliens reaching the left edge (behind the ship).
        self._check_aliens_left()

    def _check_fleet_edges(self):
        """
        Respond if any alien has reached the top or bottom screen edge.

        Calls _change_fleet_direction() to shift the fleet vertically and
        reverse its vertical drift.
        """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """
        Drop the entire fleet horizontally and reverse vertical direction.

        Each alien is nudged inward (to the left) by fleet_drop_speed pixels,
        then the fleet_direction flag is flipped so the vertical drift
        alternates between down and up.
        """
        for alien in self.aliens.sprites():
            alien.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_left(self):
        """
        Check whether any alien has reached the left edge of the screen.

        If an alien passes the left boundary (i.e., behind the ship's
        position), it counts the same as the ship being hit — a life is
        lost and the game state is reset.
        """
        for alien in self.aliens.sprites():
            if alien.rect.right <= 0:
                self._ship_hit()
                break

    def _ship_hit(self):
        """
        Respond to the ship being hit by an alien or bypassed by one.

        Decrements ships_left. If lives remain, the current fleet and
        bullets are cleared, a new fleet is created, and the ship is
        re-centered. If no lives remain, the game is set to inactive.
        """
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            # Clear aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            # Create a fresh fleet and re-center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause briefly so the player can reorient.
            pygame.time.wait(500)
        else:
            self.stats.game_active = False

    # ------------------------------------------------------------------ #
    # Screen rendering                                                     #
    # ------------------------------------------------------------------ #

    def _update_screen(self):
        """
        Redraw the screen each frame and flip to the new image.

        Fills the background, draws all bullets and aliens, draws the ship,
        and shows a simple game-over message when the game is inactive.
        """
        self.screen.fill(self.settings.bg_color)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        self.ship.blitme()

        if not self.stats.game_active:
            self._draw_game_over()

        pygame.display.flip()

    def _draw_game_over(self):
        """
        Display a 'Game Over' message in the center of the screen.

        Uses pygame's default SysFont to render white text on the
        grey background so the player knows the game has ended.
        """
        font = pygame.font.SysFont(None, 72)
        msg = font.render("GAME OVER", True, (255, 0, 0))
        msg_rect = msg.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(msg, msg_rect)


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
