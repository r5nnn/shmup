"""Module for placing and blitting player, handles user input and collision."""
from typing import override

import pygame.sprite
from .spritesheet import Spritesheet


class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_dir: str, x: int, y: int, speed: int):
        """Class for creating a sprite that a user can control.

        Extracts sprites out of the spritesheet given and creates a rect for the player at the coordinates specified.

        Args:
            sprite_dir: String of directory to sprite, without the file type ending
            x: X coordinate where to first place the sprite
            y: Y coordinate where to first place the sprite
            speed: Speed of sprite in ptx
        """
        super().__init__()
        self.speed = speed
        self.spritesheet = Spritesheet(sprite_dir)
        self.player = [[self.spritesheet.parse_sprite(f'{sprite_dir.split('\\')[-1]} {i} {x}.png') for x in range(2)] for i in ['idle', 'down', 'left',
                                                                                                                                'right', 'up']]
        self.modifier_key = 0
        self.player_state = 0
        self.rect = self.player[self.player_state][self.modifier_key].get_rect(center=(x, y))
        self.key_list = []

    @override
    def update(self) -> None:
        """Handles moving the sprite in accordance with user input."""
        self.dx, self.dy, self.player_state, self.modifier_key = 0, 0, 0, 0
        for key in self.key_list:
            if key == pygame.K_UP:
                self.dy = -self.speed
                self.player_state = 4
            elif key == pygame.K_DOWN:
                self.dy = self.speed
                self.player_state = 1
            elif key == pygame.K_LEFT:
                self.dx = -self.speed
                self.player_state = 2
            elif key == pygame.K_RIGHT:
                self.dx = self.speed
                self.player_state = 3
        if pygame.K_LSHIFT in self.key_list:
            self.dx /= 2
            self.dy /= 2
            self.modifier_key = 1
        self.rect.move_ip(self.dx, self.dy)

    def render(self, surface: pygame.Surface) -> None:
        """Handles blitting the player onto the screen.

        Makes sure player movement fits screen boundaries."""
        self.rect.clamp_ip(surface.get_rect())
        surface.blit(self.player[self.player_state][self.modifier_key], self.rect)

    def on_keydown(self, event: pygame.event.Event) -> None:
        """Handles user keydown events.

        Args:
            event: Event to handle.
        """
        self.key_list.append(event.key) if event.key not in self.key_list else None

    def on_keyup(self, event: pygame.event.Event) -> None:
        """Handles user keyup events.

        Args:
            event:  Event to handle.
        """
        self.key_list.remove(event.key) if event.key in self.key_list else None

    def on_exit(self) -> None:
        """Clears key list on exit."""
        self.key_list.clear()
