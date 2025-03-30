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

    type: Literal["player", "enemy", "playerbullet", "enemybullet", "item"] | str

    def __init__(
        self,
        spawnpoint: tuple[int, int],
        spawn_alignment: RectAlignments = "center",
        *,
        sprite: pygame.Surface | str,
        sprite_scale: int = 1,
        sprite_rect: pygame.Rect | None = None,
        rect_alignment: RectAlignments = "center",
        rect_offset: tuple[int, int] = (0, 0),
    ):
        """Base class for all the game's entities.

        :param spawnpoint: The position the entity should start at.
        :param spawn_alignment: The alignment of the spawnpoint coordinates.
        :param sprite: Either a singular surface of the sprite, or the string
        tag of the spritesheet so the sprites can be loaded using Load() and
        get_sprites()
        :param sprite_scale: The scale factor of the sprite surface.
        :param sprite_rect: An optional custom hitbox rect for the sprite for
        when the sprite_rect should be different from the size of the sprite
        surface.
        :param rect_alignment: The alignment of the sprite_rect relative to the
        sprite surface.
        :param rect_offset: The offset of the sprite_rect from the sprite
        surface.
        """
        Sprite.__init__(self)
        self.spawnpoint = spawnpoint
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
            if sprite_scale > 1:
                self.sprite = pygame.transform.scale_by(self.sprite, sprite_scale)
        self.rect = (
            sprite_rect if sprite_rect is not None else self.sprite.get_rect()
        )
        self.abs_rect = (
            self.sprite.get_rect()
            if sprite_rect is not None
            else self.rect.copy()
        )
        self.rect_alignment = rect_alignment
        self.rect_offset = rect_offset
        self.move_to_spawn()

    def move_to_spawn(self) -> None:
        """Sets the position of the entity to the spawn position.

        First sets the position of the abs_rect to the spawnpoint using the
        spawn alignment, then updates the position of the rect to match the
        abs_rect.
        """
        setattr(self.abs_rect, self.spawn_alignment, self.spawnpoint)
        setattr(
            self.rect,
            self.rect_alignment,
            self.get_rect_pos(self.rect_alignment),
        )

    def get_rect_pos(self, alignment: RectAlignments) -> list[int]:
        """Gets the position of the rect based on the position of the abs_rect.

        Adds the rect_offset to each coordinate.
        """
        return [
            coord + self.rect_offset[i]
            for i, coord in enumerate(getattr(self.abs_rect, alignment))
        ]

    def get_abs_rect_pos(self, alignment: RectAlignments) -> list[int]:
        """Gets the position of the abs_rect based on the position of the rect.

        Subtracts the rect_offset from each coordinate.
        """
        return [
            coord - self.rect_offset[i]
            for i, coord in enumerate(getattr(self.rect, alignment))
        ]

    @override
    def update(self) -> None:
        """Called every game loop to update the sprite before blitting.

        Updates the position of the rect based on the position of the abs_rect.
        Should be overriden with other updates that should happen to the
        entitiy.
        """
        setattr(
            self.rect,
            self.rect_alignment,
            self.get_rect_pos(self.rect_alignment),
        )

    def blit(self) -> None:
        """Draws the entitiy onto the screen after updating.

        Draws the current sprite onto the screen at the position of the
        absolute rect.
        """
        system_data.abs_window.blit(self.sprite, self.abs_rect)

    def on_collide(self, collided_entity: Entity) -> None:
        """Method called whenever the entity has collided with another entity.

        The collided entity is passed as a parameter.
        """


class EntityGroup(pygame.sprite.Group):
    """Child class of `pygame.sprite.Group` that includes a `blit()` method."""

    def __init__(self):
        super().__init__()

    def blit(self) -> None:
        for sprite in self.sprites():
            sprite.blit()


class Animation:
    def __init__(self, frame: str, frame_duration: int, frame_scale: int = 1, *,
                 start_playing: bool = False):
        if frame_scale > 1:
            self.frames = tuple(
                pygame.transform.scale_by(sprite, 2)
                for sprite in get_sprites(Load("image").path[frame])
            )
        else:
            self.frames = get_sprites(Load("image").path[frame])
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.time_since_last_frame = 0
        self.is_playing = start_playing
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
