"""Handles collisions with entities."""

import logging
from typing import TYPE_CHECKING

import pygame.sprite

from src.components.entities.entityutils import Entity

if TYPE_CHECKING:
    from src.states.game import Game


def update_collisions(game: "Game") -> None:
    """Checks for collisions and notifies collided sprites."""
    player_enemy_collisions = pygame.sprite.spritecollide(
        game.player, game.enemies, dokill=False
    )
    _handle_sprite_collisions(game.player, player_enemy_collisions)

    player_bullet_enemy_collisions = pygame.sprite.groupcollide(
        game.player_bullets, game.enemies, dokilla=True, dokillb=True
    )
    _handle_group_collisions(player_bullet_enemy_collisions)

    enemy_bullet_player_collisions = pygame.sprite.spritecollide(
        game.player, game.enemy_bullets, dokill=True
    )
    _handle_sprite_collisions(game.player, enemy_bullet_player_collisions)


def _handle_group_collisions(collisions: dict) -> None:
    for sprite, collided_sprites in collisions.items():
        for other_sprite in collided_sprites:
            sprite.on_collide(other_sprite)
            other_sprite.on_collide(sprite)
            logging.debug(
                "Collided %r with %r in group collision.", sprite, other_sprite
            )


def _handle_sprite_collisions(sprite: Entity, collisions: list) -> None:
    for other_sprite in collisions:
        sprite.on_collide(other_sprite)
        other_sprite.on_collide(sprite)
        logging.debug(
            "Collided %r with %r in sprite collision.", sprite, other_sprite
        )
