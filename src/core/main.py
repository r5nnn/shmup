"""Module containing the game loop and a function to quit it.

Must be initialised with `state_dict` and `start_state` otherwise a
RuntimeError will be raised.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pygame.display

from src.components import events, overlaymanager, statemanager
from src.core.data import settings, system_data
from src.core.keybinds import keybinds
from src.core.utils import toggle_flag, toggle_fullscreen
import faulthandler

faulthandler.enable()

if TYPE_CHECKING:
    from src.states.state import State

logger = logging.getLogger("src")


def init(state_dict: dict[str, type[State]], start_state: str) -> None:
    """Initialises the module with the state_dictionary and start state.

    :param state_dict: A dictionary containing the name of every game state
    bound to its class.
    :param start_state: The state which the game should start in.
    """
    statemanager.state_dict = state_dict
    statemanager.append(start_state, initial=True)


def gameloop() -> None:
    """Starts the while loop that updates the game every iteration."""
    global _running
    if statemanager.state_dict is None:
        msg = "Control module has not been initialised with state_dict."
        raise RuntimeError(msg)

    while _running:
        events.process(pygame.event.get())
        events.eventbinder.notify()
        if system_data.quit:
            logger.info("Quit set to True, saving and exiting game.")
            settings.save()
            _running = False

        statemanager.current_state().update()
        if overlay := overlaymanager.current_overlay(accept_no_overlay=True):
            overlay.update()
        statemanager.current_state().render()
        if overlay:
            overlay.render()

        system_data.dt = pygame.time.Clock().tick(165) / 1000.0
        system_data.window.blit(
            pygame.transform.scale_by(
                system_data.abs_window, system_data.scale_factor
            ),
            (0, 0),
        )
        pygame.display.flip()


_running = True

events.eventbinder.register(
    ("keydown", pygame.K_F11), action=toggle_fullscreen
)
events.eventbinder.register(
    ("keydown", pygame.K_END), action=statemanager.quit_game
)
events.eventbinder.register(
    ("key", pygame.K_LSHIFT),
    ("keydown", pygame.K_F11),
    action=lambda: toggle_flag(pygame.NOFRAME),
)
