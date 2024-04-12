"""Parent class for making and changing through states via a state stack."""
from typing import TYPE_CHECKING

import pygame

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
        self.backdrop = None

    def on_enter(self) -> None:
        """Call on being at the top of the state stack."""

    def on_exit(self) -> None:
        """Call on leaving the top of the state stack."""

    def update_state(self) -> None:
        """Call with actions to be updated within the stage."""

    def render_state(self, surface: pygame.Surface) -> None:
        """Call to blit state to surface.

        Args:
            surface: Surface which image will be blitted to.
        """
        surface.blit(self.backdrop, (0, 0)) if self.backdrop is not None else None
        if self.objects is not None:
            for obj in self.objects:
                obj.update(surface)

    def enter_state(self) -> None:
        """Append state to the top of the state stack."""
        # saves current display if there is more than one in the state stack
        self.prev_state = self.game.state_stack[-1] if len(self.game.state_stack) > 1 else self.game.title_screen
        self.game.state_stack.append(self)

    def exit_state(self) -> None:
        """Pops the state off the end of the stack."""
        self.game.state_stack.pop()
        self.game.state_stack[-1].on_enter()  # call in order to notify state underneath it has been switched to (for one time events on loading in)
