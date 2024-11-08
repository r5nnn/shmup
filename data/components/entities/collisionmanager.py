"""Handles collisions with entities."""
import logging
from typing import TYPE_CHECKING

import pygame.sprite

from data.components.entities.entity import Entity

if TYPE_CHECKING:
    from data.states.game import Game


def update(game: "Game"):
    """Checks for collisions and notifies collided sprites."""
    player_enemy_collisions = pygame.sprite.spritecollide(
        game.player, game.enemies, False)
    _handle_sprite_collisions(game.player, player_enemy_collisions)

    player_bullet_enemy_collisions = pygame.sprite.groupcollide(
        game.player_bullets, game.enemies, True, True)
    _handle_group_collisions(player_bullet_enemy_collisions)

    enemy_bullet_player_collisions = pygame.sprite.spritecollide(
        game.player, game.enemy_bullets, True)
    _handle_sprite_collisions(game.player, enemy_bullet_player_collisions)


def _handle_group_collisions(collisions: dict):
    for sprite, collided_sprites in collisions.items():
        for other_sprite in collided_sprites:
            sprite.on_collide(other_sprite)
            other_sprite.on_collide(sprite)
            logging.debug(f'Collided {repr(sprite)} with {repr(other_sprite)} '
                          f'in group collision.')


def _handle_sprite_collisions(sprite: Entity, collisions: list):
    for other_sprite in collisions:
        sprite.on_collide(other_sprite)
        other_sprite.on_collide(sprite)
        logging.debug(f'Collided {repr(sprite)} with {repr(other_sprite)} in '
                      f'sprite collision.')
