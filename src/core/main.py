"""Module containing the game loop and a function to quit it.

Must be initialised with `state_dict` and `start_state` otherwise a
RuntimeError will be raised.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import pygame.display

import src.components.input as input_manager
from src.components import InputBinder
from src.core.utils import toggle_fullscreen, toggle_flag
from src.states.managers import StateManager, OverlayManager
from src.core.data import system_data

if TYPE_CHECKING:
    from src.states.state import State


def init(state_dict: dict[str, type[State]], start_state: str) -> None:
    _state_manager.state_dict = state_dict
    _state_manager.append(start_state)


def gameloop() -> None:
    global _running
    if _state_manager.state_dict is None:
        msg = "Control module has not been initialised with state_dict."
        raise RuntimeError(msg)

    while _running:
        input_manager.process_events(pygame.event.get())
        if input_manager.get_quit():
            _running = False
        _input_binder.notify()

        _state_manager.current_state.update()
        _state_manager.current_state.render()
        if current_overlay := _overlay_manager.current_overlay:
            current_overlay.update()
            current_overlay.render()

        system_data["dt"] = _clock.tick(165) / 1000.0
        pygame.display.flip()


_running = True
_clock = pygame.time.Clock()
_input_binder = InputBinder()
_state_manager = StateManager()
_overlay_manager = OverlayManager()

_input_binder.register(("keydown", pygame.K_F11), action=toggle_fullscreen)
_input_binder.register(("keydown", pygame.K_END), action=_state_manager.quit)
_input_binder.register(("key", pygame.K_LSHIFT), ("keydown", pygame.K_F11),
                      action=lambda: toggle_flag(pygame.NOFRAME))
