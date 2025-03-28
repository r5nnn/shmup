"""Contains the base class for all the game's entities and a group for managing them."""

from __future__ import annotations

from abc import ABC
from typing import Literal, TYPE_CHECKING
from typing import override

import pygame.display
from pygame.sprite import Sprite

from src.core import system_data
from src.core.load import Load, get_sprites

if TYPE_CHECKING:
    from src.core.types import RectAlignments


class Entity(Sprite, ABC):
    """Base class for all the game's entities."""

    type: Literal["player", "enemy", "playerbullet", "enemybullet"]

    def __init__(
        self,
        spawnpoint: tuple[int, int],
        sprite: pygame.Surface | str,
        sprite_scale: int = 1,
        sprite_rect: pygame.Rect | None = None,
        rect_offset: tuple[int, int] = (0, 0),
        rect_alignment: RectAlignments = "center",
        spawn_alignment: RectAlignments = "center",
    ):
        Sprite.__init__(self)
        self.spawnpoint = spawnpoint
        self.rect_offset = rect_offset
        self.rect_alignment = rect_alignment
        self.spawn_alignment = spawn_alignment
        if isinstance(sprite, str):
            if sprite_scale > 1:
                self.sprites = tuple(
                    pygame.transform.scale_by(sprite, 2)
                    for sprite in get_sprites(Load("image").path[sprite])
                )
            else:
                self.sprites = get_sprites(Load("image").path[sprite])
            self.sprite = self.sprites[0]
        else:
            self.sprites = ()
            self.sprite = sprite
        self.rect = (
            sprite_rect if sprite_rect is not None else sprite.get_rect()
        )
        self.abs_rect = (
            self.sprite.get_rect()
            if sprite_rect is not None
            else self.rect.copy()
        )
        self.move_to_spawn()

    def move_to_spawn(self) -> None:
        setattr(self.abs_rect, self.spawn_alignment, self.spawnpoint)
        setattr(
            self.rect,
            self.rect_alignment,
            self.get_rect_pos(self.rect_alignment),
        )

    def get_rect_pos(self, alignment: RectAlignments) -> list[int]:
        return [
            coord + self.rect_offset[i]
            for i, coord in enumerate(getattr(self.abs_rect, alignment))
        ]

    def get_abs_rect_pos(self, alignment: RectAlignments) -> list[int]:
        return [
            coord - self.rect_offset[i]
            for i, coord in enumerate(getattr(self.rect, alignment))
        ]

    @override
    def update(self) -> None:
        setattr(
            self.rect,
            self.rect_alignment,
            self.get_rect_pos(self.rect_alignment),
        )

    def blit(self) -> None:
        system_data.abs_window.blit(self.sprite, self.abs_rect)

    def on_collide(self, collided_sprite: Entity) -> None: ...


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
