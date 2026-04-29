"""
Program: Alien Invasion Game
Author: Farouk Bellili
Purpose: Final submission — a side-scrolling Alien Invasion variant where the
         ship sits on the left edge, moves vertically, and fires horizontally.
         Includes a Play button, full HUD (score, high score, level, lives),
         hidden mouse cursor during play, speed scaling, and scoring.
Starter Code: Based on classroom tutorial and textbook project.
Date: 2026-04-14
"""

import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button


class AlienInvasion:
    """
    Overall class to manage game assets and behavior.

    Handles the main loop, event processing, Play button, fleet creation
    and movement, bullet/alien collisions, HUD updates, scoring, speed
    scaling, and all loss/reset conditions for the side-scrolling variant.
    """

    def __init__(self):
        """
        Initialize pygame, the display window, and all game objects.

        Creates the screen, settings, stats, scoreboard, ship, bullet and
        alien groups, the initial fleet, and the Play button. The game
        starts in an inactive state until the player clicks Play.
        """
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        # Stats must exist before Scoreboard so it can read from them.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Game starts inactive — Play button must be clicked to begin.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """
        Start the main game loop.

        Runs at 60 FPS. Game objects only update when the game is active;
        the screen is always redrawn so the Play button and HUD stay visible.
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
        Listen for and route all pygame events.

        Handles window close, keydown, keyup, and mouse click events.
        Mouse clicks are passed to _check_play_button() for hit-testing.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """
        Respond to keys being pressed down.

        UP/DOWN arrows move the ship; SPACE fires a bullet; Q quits.

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
        Respond to keys being released.

        Stops vertical ship movement when the arrow key is released.

        Args:
            event (pygame.event.Event): The keyup event to process.
        """
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _check_play_button(self, mouse_pos):
        """
        Start or restart the game when the Play button is clicked.

        Only responds if the click lands on the button AND the game is
        currently inactive, preventing accidental restarts mid-game.
        Resets all dynamic settings, stats, and HUD; rebuilds the fleet;
        re-centers the ship; and hides the mouse cursor.

        Args:
            mouse_pos (tuple): The (x, y) pixel position of the mouse click.
        """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset speed settings to baseline.
            self.settings.initialize_dynamic_settings()

            # Reset stats and refresh all HUD images.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_high_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Clear leftover aliens and bullets from the previous game.
            self.aliens.empty()
            self.bullets.empty()

            # Fresh fleet and centered ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the cursor so it doesn't distract the player.
            pygame.mouse.set_visible(False)

    # ------------------------------------------------------------------ #
    # Bullet management                                                    #
    # ------------------------------------------------------------------ #

    def _fire_bullet(self):
        """
        Create a new bullet at the ship's nose if under the bullet cap.

        Enforces the maximum number of simultaneous bullets defined in
        settings so the player cannot flood the screen with projectiles.
        """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """
        Move all bullets and cull any that have left the right edge.

        After updating positions, delegates to collision detection to
        check whether any bullet has struck an alien.
        """
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """
        Detect bullet-alien overlaps and respond.

        Uses groupcollide() to simultaneously remove any colliding bullet
        and alien. Awards points for every alien destroyed, accounting for
        multi-alien hits from a single bullet. Updates the HUD score and
        checks for a new high score after each collision batch.

        If the entire fleet is wiped out, clears bullets, creates a new
        fleet, increases game speed, and increments the level counter.
        """
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if collisions:
            for aliens_hit in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens_hit)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Level cleared — speed up and spawn a new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()

    # ------------------------------------------------------------------ #
    # Alien fleet management                                               #
    # ------------------------------------------------------------------ #

    def _create_fleet(self):
        """
        Build a full grid of aliens on the right side of the screen.

        Uses the alien's own size plus a small fixed gap to calculate how
        many rows and columns fit. The entire fleet block is then vertically
        centered on the screen so aliens appear in the middle on spawn.
        Delegates individual alien placement to _create_alien().
        """
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height

        # Generous gap so aliens have breathing room.
        gap = 20

        col_step = alien_width + gap
        row_step = alien_height + gap

        # Columns: leave one alien-width margin on each side.
        available_x = self.settings.screen_width - 2 * alien_width
        number_cols = available_x // col_step

        # Rows: reserve 80px top and bottom so no alien spawns near an edge.
        # Hard cap at 5 rows so the grid stays manageable.
        margin_y = 80
        available_y = self.settings.screen_height - 2 * margin_y
        number_rows = min(available_y // row_step, 5)

        # True vertical center: compute actual fleet height then offset.
        fleet_height = number_rows * row_step - gap
        top_offset = (self.settings.screen_height - fleet_height) // 2

        for col_number in range(number_cols):
            for row_number in range(number_rows):
                self._create_alien(col_number, row_number,
                                   col_step, row_step, top_offset)

    def _create_alien(self, col_number, row_number,
                      col_step, row_step, top_offset):
        """
        Place a single alien in the fleet grid.

        Column 0 is closest to the right edge of the screen; higher column
        numbers push aliens further right so the fleet enters from that side.
        Rows are evenly spaced and the block is vertically centered via
        top_offset.

        Args:
            col_number (int): Column index (0 = closest to right edge).
            row_number (int): Row index (0 = top row).
            col_step (int): Horizontal pixels between column starts.
            row_step (int): Vertical pixels between row starts.
            top_offset (int): Pixels from the top to start the first row.
        """
        alien = Alien(self)
        alien_width = alien.rect.width

        # Columns grow rightward from the right edge of the screen.
        alien.x = (
            self.settings.screen_width
            - alien_width
            - col_step * col_number
        )
        alien.rect.x = alien.x

        # Rows start at top_offset so the fleet is vertically centered.
        alien.rect.y = top_offset + row_step * row_number

        self.aliens.add(alien)

    def _update_aliens(self):
        """
        Update all alien positions and check for loss conditions.

        First checks whether any alien has hit a vertical screen edge so
        the fleet can bounce. Then updates all alien positions. Finally
        checks for alien-ship collision and aliens escaping the left edge.
        """
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_left()

    def _check_fleet_edges(self):
        """
        Detect whether any alien has reached the top or bottom edge.

        If so, calls _change_fleet_direction() to bounce the fleet and
        advance it horizontally toward the ship.
        """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """
        Shift the entire fleet left.

        """
        for alien in self.aliens.sprites():
            alien.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_left(self):
        """
        Check whether any alien has passed the left edge of the screen.

        In the side-scrolling variant the left edge is behind the ship.
        """
        for alien in self.aliens.sprites():
            if alien.rect.right <= 0:
                self._ship_hit()
                break

    def _ship_hit(self):
        """
        Respond to the ship being hit or an alien slipping past it.

        Decrements ships_left and refreshes the lives HUD. If lives remain,
        clears the screen, rebuilds the fleet, re-centers the ship, and
        pauses briefly. When no lives remain, deactivates the game and
        restores the mouse cursor so the player can click Play again.
        """
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            pygame.time.wait(500)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    # ------------------------------------------------------------------ #
    # Screen rendering                                                     #
    # ------------------------------------------------------------------ #

    def _update_screen(self):
        """
        Redraw every visual element.

        Draw order: background → bullets → aliens → ship → HUD → Play
        button (if inactive). The Play button is drawn last so it appears
        on top of everything when the game is not running.
        """
        self.screen.fill(self.settings.bg_color)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        self.ship.blitme()

        # HUD is always visible.
        self.sb.show_score()

        # Play button only shown when the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
