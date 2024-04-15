"""Module used for creating and handling popup screens"""
import webbrowser
from typing import TYPE_CHECKING, Callable, override

import pygame

from .modules.txt import Txt
from .state import State
from .modules.btn import BtnTxt, BtnBack

# avoids relative import error while making pycharm happy (shows error when type resides in another module when using
# PEP 563 – Postponed Evaluation of Annotations)
if TYPE_CHECKING:
    from ..game import Game


class Popup(State):
    def __init__(self, game: "Game", txt: str, btn1_txt: str, btn2_txt: str, btn1_func: Callable, btn2_func: Callable = None):
        super().__init__(game)

        # buttons
        self.btn1 = BtnTxt(self.game, 32, self.game.WINX/2 * 0.85, self.game.WINY/2, 200, 50, btn1_txt, func=btn1_func)
        if btn2_func is None:
            self.btn2 = BtnBack(self.game, 32, self.game.WINX/2 * 1.15, self.game.WINY/2, 200, 50, text=btn2_txt)
        else:
            self.btn2 = BtnTxt(self.game, 32, self.game.WINX/2 * 1.15, self.game.WINY/2, 200, 50, btn2_txt, btn2_func)

        # text
        self.txt = Txt(self.game.font_dir, 32, self.game.WINX/2, self.game.WINY/2 * 0.8, txt, "midbottom")

        # surface
        self.rect = pygame.Rect(0, 0, self.txt.rects[0].width * 1.05, (self.btn1.rect.bottom - self.txt.rects[0].top) * 1.5)
        self.rect.center = (self.game.WINX/2, self.game.WINY/2 * 0.9)
        # create surface compatible with modifying alpha (pygame.SRCALPHA)
        self.rect_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.rect_surf.set_alpha(170)  # 2/3 opacity
        pygame.draw.rect(self.rect_surf, (0, 0, 0), self.rect_surf.get_rect())

        self.objects = [[self.txt], [self.btn1, self.btn2]]

    @override
    def render_state(self, surface: pygame.Surface) -> None:
        self.prev_state.render_state(surface)
        surface.blit(self.rect_surf, self.rect_surf.get_rect(center=(self.game.WINX/2, self.game.WINY/2 * 0.9)))
        super().render_state(surface)

    def on_click(self, event: pygame.event.Event) -> None:
        """Handles clicking anywhere but the popup to exit."""
        if not self.rect.collidepoint(self.game.pos) and event.button == 1:
            self.game.back()

    def on_release(self, event: pygame.event.Event) -> None:
        ...


class PopupLink(Popup):
    def __init__(self, game: "Game", link: str):
        self.link = link
        super().__init__(game, txt=f"Open {link} in your browser?", btn1_txt="Open", btn2_txt='Cancel', btn1_func=self.open)

    def open(self) -> None:
        webbrowser.open(self.link)
        self.game.back(play_sfx=False)