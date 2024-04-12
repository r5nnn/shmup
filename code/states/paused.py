"""Used for anything related to the Paused state"""
import os
from typing import TYPE_CHECKING

import pygame

from .modules.eventmanager import generalEventManager
from .state import State
from .options import Options
from .modules.img import Img
from .modules.btn import Btn, BtnBack

# avoids relative import error while making pycharm happy (shows error when type resides in another module when using
# PEP 563 – Postponed Evaluation of Annotations)
if TYPE_CHECKING:
    from ..game import Game


class Paused(State):
    def __init__(self, game: 'Game'):
        """Initialises Paused with parent class State

        Creates all the surfaces to display.


        For additional info on args, view help on parent class State.
        """
        super().__init__(game)
        # create button background rect
        self.rect = pygame.Rect(self.game.WINX / 2, self.game.WINY / 2, self.game.WINX * 0.3, self.game.WINY * 0.5)
        # create surface compatible with modifying alpha (pygame.SRCALPHA)
        self.rect_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.rect_surf.set_alpha(128)  # half opacity
        # draw rectangle onto surface
        pygame.draw.rect(self.rect_surf, (0, 0, 0), self.rect_surf.get_rect())

        # surface
        self.paused_img = Img(self.game.WINX / 2,
                              self.rect_surf.get_rect(center=(self.game.WINX / 2, self.game.WINY / 2)).y * 1.4,
                              pygame.image.load(os.path.join(self.game.title_dir, 'paused.png')).convert(), scale=3)

        # buttons
        self.btn_resume = BtnBack(self.game, 36, self.game.WINX / 2, self.paused_img.rect.bottom * 1.1, 250, 50, 'Resume', btn_ref='midtop')
        self.btn_options = Btn(self.game, 36, self.game.WINX / 2, self.btn_resume.rect.bottom * 1.02, 250, 50, 'Options', func=self.options, btn_ref='midtop')
        self.btn_saveandexit = Btn(self.game, 36, self.game.WINX / 2, self.btn_options.rect.bottom * 1.02, 250, 50, 'Save and Exit',
                                   func=self.title, btn_ref='midtop')

        # append objects to list for iteration
        self.objects = [self.paused_img, self.btn_resume, self.btn_options, self.btn_saveandexit]

    def render_state(self, surface: pygame.Surface) -> None:
        self.prev_state.render_state(surface)
        surface.blit(self.rect_surf, self.rect_surf.get_rect(center=(self.game.WINX / 2, self.game.WINY / 2)))
        if self.objects is not None:
            for obj in self.objects:
                obj.update(surface)
        # render (not update) previous screen while showing pause screen which gives the appearance of the game being paused

    def on_enter(self) -> None:
        for i in [self.btn_options, self.btn_resume, self.btn_saveandexit]:
            generalEventManager.register(pygame.MOUSEBUTTONDOWN, i.on_click)
            generalEventManager.register(pygame.MOUSEBUTTONUP, i.on_release)

    def on_exit(self) -> None:
        for i in [self.btn_options, self.btn_resume, self.btn_saveandexit]:
            generalEventManager.deregister(pygame.MOUSEBUTTONDOWN, i.on_click)
            generalEventManager.deregister(pygame.MOUSEBUTTONUP, i.on_release)

    def title(self):
        """Pops states off the top of the state stack until at title"""
        self.on_exit()
        self.game.state_stack = [self.game.state_stack[0]]
        self.game.state_stack[-1].on_enter()

    def options(self):
        """Creates and appends Options state to the top of the state stack."""
        self.on_exit()
        options = Options(self.game, self)
        options.on_enter()
        options.enter_state()
