"""Handles anything related to the Stage1 state"""
import os
from typing import TYPE_CHECKING, override

import pygame

from .modules.collisionmanager import collisionDetector
from .modules.eventmanager import generalEventManager

from .state import State
from .paused import Paused

from .modules.entity import Enemy
from .modules.player import Player

# avoids relative import error while making pycharm happy
# (shows error when type resides in another module when using
# PEP 563 – Postponed Evaluation of Annotations)
if TYPE_CHECKING:
    from ..game import Game


class Stage1(State):
    def __init__(self, game: 'Game'):
        """
        Class for displaying the stage1 screen.
        Assigns backdrop and creates all the surfaces to display.

        Args:
            game: Class that runs the game.
        """
        super().__init__(game)
        self.backdrop = pygame.image.load(
            os.path.join(self.game.background_dir, 'stage.png')
        ).convert()

        # player
        self.players = pygame.sprite.Group()
        self.player = Player(
            self, self.game.WINX / 2, self.game.WINY / 2 * 0.8,
            250, os.path.join(self.game.player_dir, 'player'),
            pygame.image.load(os.path.join(self.game.bullet_dir, 'bullet.png'))
            .convert_alpha(), 100, {'hp': 4, 'atk': 1})
        # noinspection PyTypeChecker
        self.players.add(self.player)

        # enemies
        self.enemies = pygame.sprite.Group()
        self.enemy = Enemy(
            self, self.game.WINX/2, self.game.WINY/3,
            {'hp': 10, 'df': 0, 'atk': 1},
            img_dir=os.path.join(self.game.enemy_dir, "6"))
        # noinspection PyTypeChecker
        self.enemies.add(self.enemy)
        collisionDetector.register(self.player.bullets, self.enemies)
        collisionDetector.register(self.enemies, self.players)

    @override
    def enter_state(self) -> None:
        """Starts playing stage audio."""
        super().enter_state()
        pygame.mouse.set_visible(False)
        self.game.playing = True
        self.game.bgm.play_audio('stage1', loops=-1)
        generalEventManager.register(pygame.KEYDOWN, self.on_keydown)
        generalEventManager.register(pygame.KEYUP, self.on_keyup)

    @override
    def update_state(self) -> None:
        # update player
        self.player.update()
        self.enemies.update()
        collisionDetector.update()

    @override
    def render_state(self, surface: pygame.Surface) -> None:
        super().render_state(surface)
        self.player.render(surface)
        self.enemies.draw(surface)

    def on_keydown(self, event: pygame.event.Event) -> None:
        """Passes detected keydown events onto player for handling.

        Args:
            event: Keydown event to be passed
            """
        if event.key in [
            pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
            pygame.K_LSHIFT, pygame.K_z
        ]:
            self.player.on_keydown(event)

    def on_keyup(self, event: pygame.event.Event) -> None:
        """Passes detected keyup events onto player for handling.

        Args:
            event: Keyup event to be passed.
        """
        if event.key in [
            pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,
            pygame.K_LSHIFT, pygame.K_z
        ]:
            self.player.on_keyup(event)

    @override
    def back(self, play_sfx: bool = True):
        self.game.btn_sfx.play_audio('click', override=True) if play_sfx else None
        self.switch_state(Paused)
