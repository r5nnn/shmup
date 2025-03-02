"""Module containing the game loop and a function to quit it.

Must be initialised with `state_dict` and `start_state` otherwise a
RuntimeError will be raised.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

import pygame.display

from src.components import events
from src.core.utils import toggle_fullscreen, toggle_flag
from src.components.manager import statemanager, overlaymanager
from src.core.data import system_data, save, config, config_dir

if TYPE_CHECKING:
    from src.states.state import State


def init(state_dict: dict[str, type[State]], start_state: str) -> None:
    statemanager.state_dict = state_dict
    statemanager.append(start_state, initial=True)

def gameloop() -> None:
    global _running
    if statemanager.state_dict is None:
        msg = "Control module has not been initialised with state_dict."
        raise RuntimeError(msg)

    while _running:
        events.process(pygame.event.get())
        if system_data["quit"]:
            save(config, config_dir)
            _running = False
        events.eventbinder.notify()

        statemanager.current_state().update()
        statemanager.current_state().render()
        if overlay := overlaymanager.current_overlay(accept_no_overlay=True):
            overlay.update()
            overlay.render()

        system_data["dt"] = pygame.time.Clock().tick(165) / 1000.0
        pygame.display.flip()

_running = True

events.eventbinder.register(("keydown", pygame.K_F11),
                            action=toggle_fullscreen)
events.eventbinder.register(("keydown", pygame.K_END),
                            action=statemanager.quit_game)
events.eventbinder.register(("key", pygame.K_LSHIFT),
                            ("keydown", pygame.K_F11),
                            action=lambda: toggle_flag(pygame.NOFRAME))
