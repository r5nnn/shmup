from typing import override, TYPE_CHECKING

import pygame.sprite

from .bullet import Bullet
from .constants import rect_allignments
from .entity import Entity
from .spritesheet import SpritesheetMaker

# avoids relative import error while making pycharm happy
# (shows error when type resides in another module when using
# PEP 563 – Postponed Evaluation of Annotations)
if TYPE_CHECKING:
    from ..stage1 import Stage1


class Player(Entity):
    def __init__(self, stage: 'Stage1',
                 x: int, y: int,
                 speed: int,
                 sprite_dir: str,
                 bullet: pygame.Surface,
                 bullet_delay: int,
                 stats: dict[str, int],
                 sprite_ref: rect_allignments = 'center'):
        """
        Class for creating a sprite that a user can control.
        Extracts sprites out of the spritesheet given and creates
        a rect forthe player at the coordinates specified.

        Args:
            sprite_dir: String of directory to sprite,
            without the file type ending.
            x: X coordinate where to first place the sprite.
            y: Y coordinate where to first place the sprite.
            speed: Speed of sprite in ptx.
        """
        super().__init__(game=stage.game, img_dir=sprite_dir)
        self.stage = stage
        self.speed = speed
        self.hp, self.atk = stats['hp'], stats['atk']
        self.bullet_img = bullet
        self.bullet_delay = bullet_delay
        self.spritesheet = SpritesheetMaker(sprite_dir)
        self.bullet_sfx = self.stage.game.bullet_sfx
        self.player = [
            [self.spritesheet.parse_sprite(
                f'{sprite_dir.split('\\')[-1]} {i}{x}.png')
                for x in ['', ' mod']]
            for i in ['idle', 'down', 'left', 'right', 'up']]
        self.image = self.player[0][0]
        self.rect = self.image.get_rect()
        setattr(self.rect, sprite_ref, (x, y))
        self.mask = pygame.mask.from_surface(pygame.transform.scale_by(
            self.spritesheet.parse_sprite(
                f'{sprite_dir.split('\\')[-1]} mask.png'), 1))
        self.modifier_key = 0
        self.player_state = 0
        self.previous_time = 0
        self.rect = self.player[self.player_state][self.modifier_key] \
            .get_rect(center=(x, y))
        self.key_list = []
        self.bullets = pygame.sprite.Group()

    @override
    def update(self) -> None:
        """Handles moving the sprite in accordance with user input."""
        self.dx, self.dy, self.player_state, self.modifier_key = 0, 0, 0, False
        for key in self.key_list:
            match key:
                case pygame.K_UP:
                    self.dy = -self.speed
                    self.player_state = 4
                case pygame.K_DOWN:
                    self.dy = self.speed
                    self.player_state = 1
                case pygame.K_LEFT:
                    self.dx = -self.speed
                    self.player_state = 2
                case pygame.K_RIGHT:
                    self.dx = self.speed
                    self.player_state = 3
        if pygame.K_LSHIFT in self.key_list:
            self.dx /= 2
            self.dy /= 2
            self.modifier_key = True
        if pygame.K_z in self.key_list:
            current_time = pygame.time.get_ticks()
            if current_time - self.previous_time > self.bullet_delay:
                self.previous_time = current_time
                bullet = Bullet(self, self.bullet_img, 6)
                self.bullet_sfx.play_audio('shoot', override=True)
                # noinspection PyTypeChecker
                self.bullets.add(bullet)
        self.rect.move_ip(
            round(self.dx*self.game.dt), round(self.dy*self.game.dt))
        self.bullets.update()

    def render(self, surface: pygame.Surface) -> None:
        """
        Handles blitting the player onto the screen.
        Makes sure player movement fits screen boundaries.
        """
        self.rect.clamp_ip(surface.get_rect())
        surface.blit(self.player[self.player_state]
                     [1 if self.modifier_key else 0], self.rect)
        self.bullets.draw(surface)

    def collided(self, collider):
        """
        todo

        Args:
            collider:
        """
        if self.stage.enemies.has(collider):
            self.hp -= 1
            self.game.player_sfx.play_audio('player_die', override=True)
            self.rect.center = self.game.WINX / 2, self.game.WINY / 2

    def on_keydown(self, event: pygame.event.Event) -> None:
        """
        Handles user keydown events.

        Args:
            event: Event to handle.
        """
        self.key_list.append(event.key) \
            if event.key not in self.key_list else None

    def on_keyup(self, event: pygame.event.Event) -> None:
        """
        Handles user keyup events.

        Args:
            event:  Event to handle.
        """
        self.key_list.remove(event.key) \
            if event.key in self.key_list else None

    def on_exit(self) -> None:
        """Clears key list on exit."""
        self.key_list.clear()
