"""Contains the base class for all the game's entities and a group for managing them."""
from typing import override, Optional

import pygame.display
from pygame.sprite import Sprite

import data.core.utils
from data.components import RectAlignments
from data.core import screen


class Entity(Sprite):
    """Base class for all the game's entities."""
    def __init__(self, spawn: tuple[int, int], sprite: pygame.Surface,
                 sprite_rect: Optional[pygame.Rect] = None,
                 spawn_alignment: RectAlignments = "center"):
        Sprite.__init__(self)
        self._spawn = spawn
        self.spawn_alignment = spawn_alignment
        self.sprite = sprite
        self._rect = sprite_rect if sprite_rect is not None else sprite.get_rect()
        self._abs_rect = self.sprite.get_rect().copy()
        self.move_to_spawn()

    @property
    def spawn(self):
        return self._spawn

    @property
    def rect(self):
        return self._rect

    @property
    def abs_rect(self):
        return self._abs_rect

    def move_to_spawn(self):
        setattr(self._rect, self.spawn_alignment, self._spawn)

    @override
    def update(self):
        ...

    def blit(self):
        screen.blit(self.sprite, self._rect)

    def on_collide(self, collided_sprite):
        ...

    def __repr__(self):
        return (f"Entity(spawn={self.spawn!r}, sprite={self.sprite!r}, "
                f"sprite_rect={self.rect!r}, spawn_alignment={self.spawn_alignment})")


class EntityGroup(pygame.sprite.Group):
    """Child class of `pygame.sprite.Group` that includes a `blit()` method."""
    def __init__(self):
        super().__init__()

    def blit(self):
        for sprite in self.sprites():
            sprite.blit()


class Animation:
    def __init__(self, frames: list[pygame.Surface], frame_duration: int, *,
                 loop: bool = True):
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self.time_since_last_frame = 0
        self.is_playing = True
        self.direction = 1  # 1 for forward, -1 for backward

    def update(self):
        """Update the current frame based on time and direction (dt in milliseconds)."""
        if not self.is_playing:
            return

        self.time_since_last_frame += data.core.utils.dt

        if self.time_since_last_frame >= self.frame_duration:
            self.time_since_last_frame = 0
            self.current_frame += self.direction

            # Handle end of animation for both directions
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.is_playing = False
            elif self.current_frame < 0:
                if self.loop:
                    self.current_frame = len(self.frames) - 1
                else:
                    self.current_frame = 0
                    self.is_playing = False

    def get_frame(self):
        print(self.current_frame)
        return self.frames[self.current_frame]

    def reset(self, reverse: bool = False):
        """Reset the animation to the first frame, forward or backward."""
        self.current_frame = 0 if not reverse else len(self.frames) - 1
        self.time_since_last_frame = 0
        self.is_playing = True
        self.direction = -1 if reverse else 1

    def set_direction(self, forward: bool):
        """Set the animation direction."""
        self.direction = 1 if forward else -1
        self.is_playing = True  # Resume animation if paused
