"""Handles collisions with entities."""

from typing import TYPE_CHECKING

import pygame.sprite

from src.components.entities.entity import Entity, EntityGroup

if TYPE_CHECKING:
    from src.states.game import Game


def update_collisions(game: "Game") -> None:
    """Checks for collisions and notifies collided sprites."""
    player_enemy_collisions = pygame.sprite.spritecollide(
        game.player, game.enemies, dokill=False
    )
    handle_sprite_collisions(game.player, player_enemy_collisions)

    player_bullet_enemy_collisions = pygame.sprite.groupcollide(
        game.player_bullets, game.enemies, dokilla=True, dokillb=True
    )
    handle_group_collisions(player_bullet_enemy_collisions)
    print(*[f"{sprite} bullet" for sprite in game.player_bullets.sprites()])
    print(*[f"{enemy} enemy" for enemy in game.enemies.sprites()])

    enemy_bullet_player_collisions = pygame.sprite.spritecollide(
        game.player, game.enemy_bullets, dokill=True
    )
    handle_sprite_collisions(game.player, enemy_bullet_player_collisions)

    enemy_drop_player_collisions = pygame.sprite.spritecollide(
        game.player, game.enemy_drops, dokill=True, collided=abs1_spritecollide
    )
    handle_sprite_collisions(game.player, enemy_drop_player_collisions)


def handle_group_collisions(collisions: dict) -> None:
    print("che", collisions.items())
    for sprite, collided_sprites in collisions.items():
        print(sprite, collided_sprites, "check")
        for other_sprite in collided_sprites:
            print(sprite, other_sprite, "checking")
            sprite.on_collide(other_sprite)
            other_sprite.on_collide(sprite)


def handle_sprite_collisions(sprite: Entity, collisions: list) -> None:
    for other_sprite in collisions:
        sprite.on_collide(other_sprite)
        other_sprite.on_collide(sprite)


def abs1_spritecollide(sprite1: Entity, sprite2: Entity) -> bool:
    return sprite1.abs_rect.colliderect(sprite2.rect)
