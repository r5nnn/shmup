from collections import defaultdict
from typing import TYPE_CHECKING, override

import pygame.sprite

from .observer import _Observer

# avoids relative import error while making pycharm happy
# (shows error when type resides in another module when using
# PEP 563 – Postponed Evaluation of Annotations)
if TYPE_CHECKING:
    from .entity import Entity


class CollisionDetector:
    def __init__(self):
        """
        todo
        """
        self.collision_checks: dict[pygame.sprite.Group,
                                    list[pygame.sprite.Group]] \
            = defaultdict(list)

    def register(self, group: pygame.sprite.Group,
                 collision_group: pygame.sprite.Group) -> None:
        """
        Registers 2 sprites which should collide with each other.

        Args:
            group: Sprite that should collide with collision_group.
            collision_group: Sprite that should collide with group.
        """
        self.collision_checks[collision_group].append(group) \
            if group not in self.collision_checks[collision_group] else None

    def deregister(self, group: pygame.sprite.Group,
                   group_key: pygame.sprite.Group) -> None:
        """
        todo

        Args:
            group:
            group_key:
        """
        if group in self.collision_checks:
            self.collision_checks[group] = \
                [_collision_group
                 for _collision_group in self.collision_checks[group]
                 if _collision_group != group_key]
        elif group_key in self.collision_checks:
            self.collision_checks[group_key] = \
                [_group for _group in self.collision_checks[group_key]
                 if _group != group]

    # noinspection PyTypeChecker
    def update(self):
        for group_key in self.collision_checks:
            for group in self.collision_checks[group_key]:
                if sprite_dict := pygame.sprite.groupcollide(
                        group_key, group, False, False,
                        pygame.sprite.collide_mask):
                    for sprite in sprite_dict:
                        for sprite_collider in sprite_dict[sprite]:
                            sprite.collided(sprite_collider)


class CollisionHandler(_Observer):
    managers = dict()

    def __init__(self, name: str):
        """
        todo

        Args:
            name:
        """
        super().__init__(name)

    @override
    def notify(self, sprite: "Entity", sprite1: "Entity") -> None:
        """
        todo

        Args:
            sprite:
            sprite1:
        """
        sprite.collided(sprite1)


collisionDetector = CollisionDetector()
collisionHandler = CollisionHandler.get("Game Collisions")
