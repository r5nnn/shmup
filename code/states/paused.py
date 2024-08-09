"""Handles anything related to the Paused state"""
import os
from typing import TYPE_CHECKING, override

import pygame

from .modules.eventmanager import generalEventManager
from .state import State
from .options import Options
from .modules.img import Img
from .modules.btn import BtnTxt, BtnBack

# avoids relative import error while making pycharm happy (shows error when type resides in another module when using
# PEP 563 – Postponed Evaluation of Annotations)
if TYPE_CHECKING:
    from ..game import Game


class Paused(State):
    def __init__(self, game: 'Game'):
        """Initialises Paused with parent class State.

        Creates all the surfaces to display.

        For additional info on args, view help on parent class State.
        """
        super().__init__(game)
        # create window background rect
        self.rect = pygame.Rect(0, 0, self.game.WINX, self.game.WINY)
        # create surface compatible with modifying alpha (pygame.SRCALPHA)
        self.rect_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.rect_surf.set_alpha(128)  # half opacity
        # draw rectangle onto surface
        pygame.draw.rect(self.rect_surf, (0, 0, 0), self.rect)

        # surface
        self.paused_img = Img(self.game.WINX / 2,
                              self.game.WINY / 2 * 0.75,
                              pygame.image.load(os.path.join(self.game.title_dir, 'paused.png')).convert(), scale=3, ref='center')

        # buttons
        self.btn_resume = BtnBack(self.game, 36, self.game.WINX / 2, self.paused_img.img_rect.bottom * 1.1, 250, 50, 'Resume', btn_ref='midtop')
        self.btn_options = BtnTxt(self.game, 36, self.game.WINX / 2, self.btn_resume.rect.bottom * 1.02, 250, 50, 'Options',
                                  func=lambda: self.switch_state(Options), btn_ref='midtop')
        self.btn_saveandexit = BtnTxt(self.game, 36, self.game.WINX / 2, self.btn_options.rect.bottom * 1.02, 250, 50, 'Save and Exit',
                                      func=self.title, btn_ref='midtop')

        # append objects to list for iteration
        self.objects = [[self.paused_img], [self.btn_resume, self.btn_options, self.btn_saveandexit]]

    @override
    def render_state(self, surface: pygame.Surface) -> None:
        self.prev_state.render_state(surface)
        surface.blit(self.rect_surf, self.rect_surf.get_rect(center=(self.game.WINX / 2, self.game.WINY / 2)))
        super().render_state(surface)

    @override
    def enter_state(self) -> None:
        super().enter_state()
        pygame.mouse.set_visible(True)
        generalEventManager.deregister(pygame.KEYDOWN, self.prev_state.on_keydown)
        generalEventManager.deregister(pygame.KEYUP, self.prev_state.on_keyup)
        self.prev_state.player.on_exit()

    @override
    def exit_state(self) -> None:
        super().exit_state()
        pygame.mouse.set_visible(False)
        self.game.bgm.play_audio('stage1', loops=-1)
        generalEventManager.register(pygame.KEYDOWN, self.game.state_stack[-1].on_keydown)
        generalEventManager.register(pygame.KEYUP, self.game.state_stack[-1].on_keyup)

    def title(self):
        """Pops states off the top of the state stack until at title"""
        self.game.state_stack[0].enter_state()
        self.game.state_stack = [self.game.state_stack[0]]
