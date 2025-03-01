"""Module containing the game loop and a function to quit it.

Must be initialised with `state_dict` and `start_state` otherwise a
RuntimeError will be raised.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import pygame.display

from src.components import events
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
        events.process(pygame.event.get())
        if system_data["quit"]:
            _running = False
        events.binder.notify()

        _state_manager.current_state.update()
        _state_manager.current_state.render()
        if current_overlay := _overlay_manager.current_overlay:
            current_overlay.update()
            current_overlay.render()

        system_data["dt"] = _clock.tick(165) / 1000.0
        pygame.display.flip()


_running = True
_clock = pygame.time.Clock()
_state_manager = StateManager()
_overlay_manager = OverlayManager()

events.binder.register(("keydown", pygame.K_F11), action=toggle_fullscreen)
events.binder.register(("keydown", pygame.K_END), action=_state_manager.quit)
events.binder.register(("key", pygame.K_LSHIFT), ("keydown", pygame.K_F11),
                      action=lambda: toggle_flag(pygame.NOFRAME))
