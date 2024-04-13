import pygame

from .modules.eventmanager import generalEventManager
from .modules.txt import Txt
from .state import State
from .modules.btn import BtnTxt, BtnBack


class Popup(State):
    def __init__(self, game, txt, btn1_txt, btn2_txt, btn1_func, btn2_func=None):
        super().__init__(game)
        self.btn1 = BtnTxt(self.game, 32, self.game.WINX/2 * 0.85, self.game.WINY/2, 200, 50, btn1_txt, func=btn1_func)
        if btn2_func is None:
            self.btn2 = BtnBack(self.game, 32, self.game.WINX/2 * 1.15, self.game.WINY/2, 200, 50, text=btn2_txt)
        else:
            self.btn2 = BtnTxt(self.game, 32, self.game.WINX/2 * 1.15, self.game.WINY/2, 200, 50, btn2_txt, btn2_func)
        self.txt = Txt(self.game.font_dir, 32, self.game.WINX/2, self.game.WINY/2 * 0.8, txt, 'midbottom')
        self.rect = pygame.Rect(0, 0, self.txt.rects[0].width * 1.05, (self.btn1.rect.bottom - self.txt.rects[0].top) * 1.5)
        self.rect.center = (self.game.WINX/2, self.game.WINY/2 * 0.9)
        # create surface compatible with modifying alpha (pygame.SRCALPHA)
        self.rect_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.rect_surf.set_alpha(170)  # 2/3 opacity
        # draw rectangle onto surface
        pygame.draw.rect(self.rect_surf, (0, 0, 0), self.rect_surf.get_rect())
        self.objects = [self.btn1, self.btn2, self.txt]

    def render_state(self, surface: pygame.Surface) -> None:
        self.prev_state.render_state(surface)
        surface.blit(self.rect_surf, self.rect_surf.get_rect(center=(self.game.WINX/2, self.game.WINY/2 * 0.9)))
        if self.objects is not None:
            for obj in self.objects:
                obj.update(surface)
        # render (not update) previous screen while showing pause screen which gives the appearance of the game being paused

    def on_enter(self) -> None:
        for i in [self.btn1, self.btn2, self]:
            generalEventManager.register(pygame.MOUSEBUTTONDOWN, i.on_click)
            generalEventManager.register(pygame.MOUSEBUTTONUP, i.on_release)

    def on_exit(self) -> None:
        for i in [self.btn1, self.btn2, self]:
            generalEventManager.deregister(pygame.MOUSEBUTTONDOWN, i.on_click)
            generalEventManager.deregister(pygame.MOUSEBUTTONUP, i.on_release)

    def on_click(self, event) -> None:
        if not self.rect.collidepoint(self.game.pos) and event.button == 1:
            self.game.back()

    def on_release(self, event) -> None:
        ...
