"""Handles anything related to the Stage1 state"""
import os
from typing import TYPE_CHECKING, override

import pygame

from .modules.collisionmanager import collisionDetector
from .modules.entity import Enemy
from .modules.eventmanager import generalEventManager
from .state import State
from .modules.player import Player

# avoids relative import error while making pycharm happy (shows error when type resides in another module when using
# PEP 563 – Postponed Evaluation of Annotations)
if TYPE_CHECKING:
    from ..game import Game


class Stage1(State):
    def __init__(self, game: 'Game'):
        """Initialises Stage1 with parent class State.

        Creates all the surfaces to display.

        For additional info on args, view help on parent class State."""
        super().__init__(game)
        self.backdrop = pygame.image.load(os.path.join(self.game.background_dir, 'stage.png')).convert()
        self.bgm = pygame.mixer.Sound(file=self.game.stage1_music)  # make sure to keep file=self.filepath as stated by the pygame docs:
        # From https://www.pygame.org/docs/ref/mixer.html#pygame.mixer.Sound: A Unicode string can only be a file pathname. A bytes object can be either a
        # pathname or a buffer object. Use the 'file' or 'buffer' keywords to avoid ambiguity; otherwise Sound may guess wrong.
        self.bgm.set_volume(0.2)

        # player
        self.players = pygame.sprite.Group()
        self.player = Player(self, self.game.WINX / 2,
                             self.game.WINY / 2 * 0.8, 2, os.path.join(self.game.player_dir, 'player'),
                             pygame.image.load(os.path.join(self.game.bullet_dir, 'bullet.png')).convert_alpha(), 100,
                             os.path.join(self.game.sfx_dir, 'shoot.wav'))
        self.players.add(self.player)

        # enemies
        self.enemies = pygame.sprite.Group()
        self.enemy = Enemy(self, self.game.WINX/2, self.game.WINY/3, img_dir=os.path.join(self.game.enemy_dir, "bystander"))
        # noinspection PyTypeChecker
        self.enemies.add(self.enemy)
        collisionDetector.register(self.player.bullets, self.enemies)
        collisionDetector.register(self.enemies, self.players)


    @override
    def on_enter(self) -> None:
        """Starts playing stage audio."""
        super().on_enter()
        pygame.mouse.set_visible(False)
        self.game.playing = True
        # fadeout menu music
        self.game.channel_bgm.fadeout(1000)
        # start playing background music if it wasnt already playing
        if not self.game.channel_bgm_s1.get_busy():
            self.game.channel_bgm_s1.play(self.bgm, loops=-1)
        generalEventManager.register(pygame.KEYDOWN, self.on_keydown)
        generalEventManager.register(pygame.KEYUP, self.on_keyup)

    @override
    def on_exit(self) -> None:
        pygame.mouse.set_visible(True)
        generalEventManager.deregister(pygame.KEYDOWN, self.on_keydown)
        generalEventManager.deregister(pygame.KEYUP, self.on_keyup)
        self.player.on_exit()

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
        if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LSHIFT, pygame.K_z]:
            self.player.on_keydown(event)

    def on_keyup(self, event: pygame.event.Event) -> None:
        """Passes detected keyup events onto player for handling.

        Args:
            event: Keyup event to be passed.
        """
        if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_LSHIFT, pygame.K_z]:
            self.player.on_keyup(event)
