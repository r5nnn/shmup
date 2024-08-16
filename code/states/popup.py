"""Module used for creating and handling popup screens"""
import webbrowser
from typing import TYPE_CHECKING, Callable, override

import pygame

from .modules.eventmanager import generalEventManager
from .modules.txt import Txt
from .modules.txtinput import TextInputManager, TextInputVisualizer
from .state import State
from .modules.btn import BtnTxt, BtnBack

# avoids relative import error while making pycharm happy
# (shows error when type resides in another module when using
# PEP 563 – Postponed Evaluation of Annotations)
if TYPE_CHECKING:
    from ..game import Game


class Popup(State):
    def __init__(self,
                 game: "Game",
                 txt: str,
                 btn1_txt: str,
                 btn2_txt: str,
                 btn1_func: Callable = None,
                 btn2_func: Callable = None,
                 func1_exit: bool = False):
        super().__init__(game)
        self.func1_exit = func1_exit

        # buttons
        self.btn1 = BtnTxt(self.game,
                           (self.game.WINX / 2 * 0.85,
                            self.game.WINY / 2), 200, 50,
                           btn1_txt, font_size=32,
                           func=lambda: self._func(btn1_func))
        if btn2_func is None:
            self.btn2 = BtnBack(self.game,
                                (self.game.WINX / 2 * 1.15,
                                 self.game.WINY / 2), 200, 50,
                                font_size=32, text=btn2_txt)
        else:
            self.btn2 = BtnTxt(self.game,
                               (self.game.WINX / 2 * 1.15,
                                self.game.WINY / 2), 200, 50,
                               btn2_txt, btn2_func, font_size=32)

        # text
        self.txt = Txt((self.game.WINX / 2, self.game.WINY / 2 * 0.8),
                       txt, allign="midbottom", size=32)

        # surface
        self.rect = pygame.Rect(
            0, 0, self.txt.rects[0].width * 1.05,
            (self.btn1.rect.bottom - self.txt.rects[0].top) * 1.5
            )
        self.rect.center = (self.game.WINX / 2, self.game.WINY / 2 * 0.9)
        # create surface compatible with modifying alpha (pygame.SRCALPHA)
        self.rect_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.rect_surf.set_alpha(170)  # 2/3 opacity
        pygame.draw.rect(self.rect_surf, (0, 0, 0), self.rect_surf.get_rect())

        self.objects = [[self.txt], [self.btn1, self.btn2]]

    @override
    def render_state(self, surface: pygame.Surface) -> None:
        self.prev_state.render_state(surface)
        surface.blit(self.rect_surf, self.rect_surf.get_rect(
            center=(self.game.WINX / 2, self.game.WINY / 2 * 0.9)))
        super().render_state(surface)

    def on_click(self, event: pygame.event.Event) -> None:
        """Handles clicking anywhere but the popup to exit."""
        if not self.rect.collidepoint(self.game.pos) and event.button == 1:
            self.back()

    def on_release(self, event: pygame.event.Event) -> None:
        ...

    def _func(self, func, *args):
        if self.func1_exit:
            self.exit_state()
        func(*args)

    @override
    def enter_state(self) -> None:
        super().enter_state()
        generalEventManager.register(pygame.MOUSEBUTTONDOWN, self.on_click)
        generalEventManager.register(pygame.MOUSEBUTTONUP, self.on_release)

    @override
    def exit_state(self) -> None:
        generalEventManager.deregister(pygame.MOUSEBUTTONDOWN, self.on_click)
        generalEventManager.deregister(pygame.MOUSEBUTTONUP, self.on_release)
        super().exit_state()


class PopupLink(Popup):
    def __init__(self, game: "Game", link: str):
        self.link = link
        super().__init__(game, txt=f"Open {link} in your browser?",
                         btn1_txt="Open", btn2_txt='Cancel',
                         btn1_func=self.open)

    def open(self) -> None:
        webbrowser.open(self.link)
        self.back(play_sfx=False)


class PopupTextbox(Popup):
    def __init__(self,
                 game: "Game",
                 txt: str,
                 btn1_txt: str,
                 btn2_txt: str,
                 btn1_func: Callable = None,
                 btn2_func: Callable = None,
                 func1_exit: bool = False,
                 font: pygame.font.Font = None,
                 font_size: int = None):
        super().__init__(game, txt, btn1_txt, btn2_txt,
                         btn1_func, btn2_func, func1_exit)
        self.textinput_manager = TextInputManager(
            validator=lambda text: len(text) <= 29)
        self.textinput = TextInputVisualizer(
            manager=self.textinput_manager,
            font_object=font if font is not None else
            pygame.font.Font(self.game.font_dir, font_size)
        )

    def render_state(self, surface: pygame.Surface) -> None:
        super().render_state(surface)
        surface.blit(
            self.textinput.surface, (self.rect.left + 10,
                                     self.txt.rects[0].bottom + 20)
        )

    def enter_state(self) -> None:
        super().enter_state()
        generalEventManager.register(pygame.KEYDOWN, self.textinput.update)

    def exit_state(self) -> None:
        generalEventManager.deregister(pygame.KEYDOWN, self.textinput.update)
        super().exit_state()

    def _func(self, func, *args):
        if len(self.textinput_manager.value) > 0:
            super()._func(func, self.textinput.value)