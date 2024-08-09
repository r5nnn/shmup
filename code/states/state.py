"""Parent class for making and changing through states via a state stack."""
from typing import TYPE_CHECKING

import pygame

from .modules.eventmanager import generalEventManager, keyEventManager

if TYPE_CHECKING:
    from ..game import Game


class State:

    def __init__(self, game: 'Game'):
        """
        Args:
            game: Script for running game
        """
        self.game = game
        self.objects = None
        self.groups = None
        self.backdrop = None

    def update_state(self) -> None:
        """Call with actions to be updated within the stage."""

    def render_state(self, surface: pygame.Surface) -> None:
        """Call to blit state to surface.
        Args:
            surface: Surface which image will be blitted to.
        """
        surface.blit(self.backdrop, (0, 0)) if self.backdrop is not None else None
        if self.objects is not None:
            for objects in self.objects:
                for obj in objects:
                    obj.update(surface)
        if self.groups is not None:
            for arr in self.groups:
                for groups in arr:
                    groups.draw(surface)
            for groups in self.groups[1]:
                groups.update()

    def unbind_keys(self) -> None:
        """Call before leaving the top of the state stack when another state is appended to the top."""
        keyEventManager.deregister(pygame.K_ESCAPE, self.back)
        for i in self.objects[1] if self.objects is not None else []:
            generalEventManager.deregister(pygame.MOUSEBUTTONDOWN, i.on_click)
            generalEventManager.deregister(pygame.MOUSEBUTTONUP, i.on_release)

    def bind_keys(self) -> None:
        """Call after entering the top of the state stack."""
        keyEventManager.register(pygame.K_ESCAPE, self.back)
        for i in self.objects[1] if self.objects is not None else []:
            generalEventManager.register(pygame.MOUSEBUTTONDOWN, i.on_click)
            generalEventManager.register(pygame.MOUSEBUTTONUP, i.on_release)

    def enter_state(self) -> None:
        """Append state to the top of the state stack."""
        # saves current display if there is more than one in the state stack
        self.prev_state = self.game.state_stack[-1] if len(self.game.state_stack) > 1 else self.game.title_screen
        self.prev_state.unbind_keys()
        self.game.state_stack.append(self)
        self.bind_keys()

    def exit_state(self) -> None:
        """Pops the state off the end of the stack."""
        self.unbind_keys()
        self.game.state_stack.pop()
        self.game.state_stack[-1].bind_keys()

    def switch_state(self, state: type, *args, **kwargs) -> None:
        """Exits current state and appends given state to the end of the stack.

        Args:
            state: The state to switch to.
            args: any additional arguments to pass to state"""
        new_state = state(self.game, *args, **kwargs)
        new_state.enter_state()
    
    def back(self, play_sfx: bool = True):
        """Pops top item out of state stack. Must be overriden in specific cases."""
        self.game.btn_sfx.force_play_audio('click') if play_sfx else None
        self.exit_state()
        