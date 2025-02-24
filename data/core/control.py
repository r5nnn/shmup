"""Module containing the game loop and a function to quit it.

Must be initialised with `state_dict` and `start_state` otherwise a RuntimeError will be
raised.
"""
from __future__ import annotations

import pygame.display

from data.core.utils import toggle_fullscreen, toggle_flag
import data.core.utils
import data.components.input as InputManager
from data.components.input import InputBinder
from data.states.state import State, state_manager


def initialise(state_dict: dict[str, type[State]], start_state: str) -> None:
    state_manager.state_dict = state_dict
    state_manager.append(start_state)




def main() -> None:
    global _running
    if state_manager.state_dict is None:
        msg = "Control module has not been initialised with state_dict."
        raise RuntimeError(msg)

    while _running:
        InputManager.process_events(pygame.event.get())
        if InputManager.get_quit():
            _running = False
        InputBinder.notify()

        state_manager.current_state.update()
        state_manager.current_state.render()

        data.core.utils.dt = _clock.tick(165) / 1000.0
        pygame.display.flip()


_running = True
_clock = pygame.time.Clock()


InputBinder.register(("keydown", pygame.K_F11),
                     action=toggle_fullscreen)
InputBinder.register(("keydown", pygame.K_END), action=state_manager.quit)
InputBinder.register(("key", pygame.K_LSHIFT), ("keydown", pygame.K_F11),
                     action=lambda: toggle_flag(flag=pygame.NOFRAME))
