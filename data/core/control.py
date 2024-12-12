"""Module containing the game loop and a function to quit it.

Must be initialised with `state_dict` and `start_state` otherwise a RuntimeError will be
raised.
"""
from __future__ import annotations

import warnings

import pygame.display

import data.components.input as InputManager
import data.core.utils
from data.components.input import InputBinder
from data.core import screen
from data.core.utils import FLAG_NAMES
from data.states.state import State, state_manager
from data.core.data import GameData


def initialise(state_dict: dict[str, type[State]], start_state: str) -> None:
    state_manager.quit_game = quit_game
    state_manager.state_dict = state_dict
    state_manager.append(start_state)


def _toggle_flag(flag: int) -> None:
    toggleable_tags = (pygame.SCALED | pygame.NOFRAME | pygame.FULLSCREEN)
    if not flag & toggleable_tags:
        warnings.warn(f"Attempted to toggle untoggleable tag: "
                      f"{FLAG_NAMES.get(flag, f"Unknown flag: ({flag})")}",
                      stacklevel=2)
    else:
        current_togglable_flags = pygame.display.get_surface().get_flags() & toggleable_tags
        print(screen.get_flags() & pygame.FULLSCREEN, pygame.FULLSCREEN)
        pygame.display.set_mode((1920, 1080), current_togglable_flags ^ flag)


def main() -> None:
    if state_manager.state_dict is None:
        msg = "Control module has not been initialised with state_dict."
        raise RuntimeError(msg)

    while _running:
        InputManager.process_events(pygame.event.get())
        if InputManager.get_quit():
            quit_game()
        InputBinder.notify()

        state_manager.current_state.update()
        state_manager.current_state.render()

        data.core.utils.dt = _clock.tick(GameData.refresh_rate) / 1000.0
        pygame.display.flip()


def quit_game() -> None:
    global _running
    _running = False


_running = True
_clock = pygame.time.Clock()

InputBinder.register(("keydown", pygame.K_F11),
                     action=pygame.display.toggle_fullscreen)
InputBinder.register(("keydown", pygame.K_END), action=quit_game)
InputBinder.register(("key", pygame.K_LSHIFT), ("keydown", pygame.K_F11),
                     action=lambda: _toggle_flag(pygame.NOFRAME))
