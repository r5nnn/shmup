"""Contains the base class for all the game's entities and a group for managing them."""
from __future__ import annotations

from typing import TYPE_CHECKING
from typing import override

import pygame.display
from pygame.sprite import Sprite

from data.core import screen

if TYPE_CHECKING:
    from data.components import RectAlignments


class Entity(Sprite):
    """Base class for all the game's entities."""

    def __init__(self, spawn: tuple[int, int], sprite: pygame.Surface,
                 sprite_rect: pygame.Rect | None = None,
                 spawn_alignment: RectAlignments = "center"):
        Sprite.__init__(self)
        self._spawn = spawn
        self.spawn_alignment = spawn_alignment
        self.sprite = sprite
        self._rect = sprite_rect if sprite_rect is not None else sprite.get_rect()
        self._abs_rect = self.sprite.get_rect().copy()
        self.move_to_spawn()

    @property
    def spawn(self) -> tuple[int, int]:
        return self._spawn

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    @property
    def abs_rect(self) -> pygame.Rect:
        return self._abs_rect

    def move_to_spawn(self) -> None:
        setattr(self._rect, self.spawn_alignment, self._spawn)

    @override
    def update(self) -> None:
        ...

    def blit(self) -> None:
        screen.blit(self.sprite, self._rect)

    def on_collide(self, collided_sprite: Entity) -> None:
        ...

    def __repr__(self):
        return (f"Entity(spawn={self.spawn!r}, sprite={self.sprite!r}, "
                f"sprite_rect={self.rect!r}, spawn_alignment={self.spawn_alignment})")


class EntityGroup(pygame.sprite.Group):
    """Child class of `pygame.sprite.Group` that includes a `blit()` method."""

    def __init__(self):
        super().__init__()

    def blit(self) -> None:
        for sprite in self.sprites():
            sprite.blit()


class Animation:
    def __init__(self, frames: list[pygame.Surface], frame_duration: int):
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.time_since_last_frame = 0
        self.is_playing = True
        self.direction = 1

    def update(self) -> None:
        """Update the current frame based on time and direction (dt in milliseconds)."""
        if not self.is_playing:
            return

        current_time = pygame.time.get_ticks()

        if current_time - self.time_since_last_frame >= self.frame_duration:
            self.time_since_last_frame = current_time
            self.current_frame += self.direction

            # Handle end of animation for both directions
            if self.current_frame >= len(self.frames):
                    self.current_frame = len(self.frames) - 1
                    self.is_playing = False
            elif self.current_frame < 0:
                    self.current_frame = 0
                    self.is_playing = False

    def get_frame(self) -> pygame.Surface:
        return self.frames[self.current_frame]

    def reset(self, *, reverse: bool = False) -> None:
        """Reset the animation to the first frame, forward or backward."""
        self.current_frame = 0 if not reverse else len(self.frames) - 1
        self.time_since_last_frame = 0
        self.is_playing = True
        self.direction = -1 if reverse else 1

    def set_direction(self, *, forward: bool) -> None:
        """Set the animation direction."""
        self.direction = 1 if forward else -1
