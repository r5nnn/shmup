from typing import TYPE_CHECKING

import pygame.sprite

from data.components.entities.entity import Entity
from data.core import Singleton

if TYPE_CHECKING:
    from data.states.game import Game


class CollisionManager(metaclass=Singleton):
    def __init__(self, game: "Game"):
        self.game = game

    def update(self):
        # Player and enemy collision
        player_enemy_collisions = pygame.sprite.spritecollide(
            self.game.player, self.game.enemies, False)
        self._handle_sprite_collisions(self.game.player,
                                       player_enemy_collisions)

        # Player bullet and enemy collision
        player_bullet_enemy_collisions = pygame.sprite.groupcollide(
            self.game.player_bullets, self.game.enemies, True, True
        )
        self._handle_group_collisions(player_bullet_enemy_collisions)

        # Enemy bullet and player collision
        enemy_bullet_player_collisions = pygame.sprite.spritecollide(
            self.game.player, self.game.enemy_bullets, True)
        self._handle_sprite_collisions(self.game.player,
                                       enemy_bullet_player_collisions)

    @staticmethod
    def _handle_group_collisions(collisions: dict):
        for sprite, collided_sprites in collisions.items():
            for other_sprite in collided_sprites:
                sprite.on_collide(other_sprite)
                other_sprite.on_collide(sprite)

    @staticmethod
    def _handle_sprite_collisions(sprite: Entity, collisions: list):
        for other_sprite in collisions:
            sprite.on_collide(other_sprite)
            other_sprite.on_collide(sprite)