import typing
from typing import TYPE_CHECKING

import pygame

from .modules.eventmanager import generalEventManager, keyEventManager

# avoids relative import error while making pycharm happy
# (shows error when type resides in another module when using
# PEP 563 – Postponed Evaluation of Annotations)
if TYPE_CHECKING:
    from ..game import Game


class State:

    def __init__(self, game: 'Game'):
        """
        Parent class for making and changing through states via a state stack.

        Examples:
            # avoid creating class in the game loop, it causes lag,
            # instead init the state before, then just enter the state.
            s = State(game)

            while True:
                if something_happens:
                    s.enter_state()
                s.update_state()
                s.render_state(surface)

        Args:
            game: Class that runs the game.
        """
        self.game = game
        self.buttons = []
        self.groups = None
        self.backdrop = None

    def update_state(self) -> None:
        """Call with actions to be updated within the stage."""

    def render_state(self, surface: pygame.Surface) -> None:
        """
        Call to render state to surface.

        Args:
            surface: Surface which state will be rendered to.
        """
        for button in self.buttons:
            button.update(surface)
        if self.groups is not None:
            for arr in self.groups:
                for groups in arr:
                    groups.draw(surface)
            for groups in self.groups[1]:
                groups.update()

    def bind_keys(self) -> None:
        """
        Binds all universal keybinds and object specific keybinds.
        Iterates through self.objects[1] and registers the objects to
        mouse inputs.
        """
        keyEventManager.register(pygame.K_ESCAPE, self.back)
        for button in self.buttons if self.buttons is not None else []:
            generalEventManager.register(
                pygame.MOUSEBUTTONDOWN, button.on_click)
            generalEventManager.register(
                pygame.MOUSEBUTTONUP, button.on_release)

    def unbind_keys(self) -> None:
        """
        Unbinds all universal keybinds and object specific keybinds.
        Iterates through self.objects[1] and deregisters the objects to
        mouse inputs.
        """
        keyEventManager.deregister(pygame.K_ESCAPE, self.back)
        for button in self.buttons if self.buttons is not None else []:
            generalEventManager.deregister(
                pygame.MOUSEBUTTONDOWN, button.on_click)
            generalEventManager.deregister(
                pygame.MOUSEBUTTONUP, button.on_release)

    def enter_state(self) -> None:
        """Appends state to the top of the state stack."""
        # saves current display if there is more than one in the state stack
        self.prev_state = self.game.state_stack[-1] \
            if len(self.game.state_stack) > 1 else self.game.title_screen
        self.prev_state.unbind_keys()
        self.game.state_stack.append(self)
        self.bind_keys()

    def exit_state(self) -> None:
        """Pops the state off the end of the stack."""
        self.unbind_keys()
        self.game.state_stack.pop()
        self.game.state_stack[-1].bind_keys()

    def switch_state(self, state: type, *args, **kwargs) -> None:
        """
        Exits current state and appends given state to the end of the stack.

        Args:
            state: The state to switch to.
            args: any additional arguments to pass to state.
            kwargs: any additional keyword arguments to pass to the state.
        """
        new_state = state(self.game, *args, **kwargs)
        new_state.enter_state()
    
    def back(self, play_sfx: bool = True):
        """
        Pops top item out of state stack.
        Must be overriden in specific cases such as where there is no state to
        exit to.
        """
        self.game.btn_sfx.play_audio('click', override=True) \
            if play_sfx else None
        self.exit_state()
