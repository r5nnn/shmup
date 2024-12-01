"""Module containing the game loop and a function to quit it.

Must be initialised with `state_dict` and `start_state` otherwise a RuntimeError will be
raised.
"""
from __future__ import annotations

import pygame.display

import data.components.input as InputManager
import data.core.utils
from data.components.input import InputBinder
from data.states.state import State, state_manager


def initialise(state_dict: dict[str, type[State]], start_state: str) -> None:
    state_manager.quit_game = quit_game
    state_manager.state_dict = state_dict
    state_manager.append(start_state)


def _toggle_tag(tag: int) -> None:
    global _screen_flags
    _screen_flags ^= tag
    pygame.display.set_mode((1920, 1080), _screen_flags)


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

        data.core.utils.dt = _clock.tick(_refresh_rate) / 1000.0
        pygame.display.flip()


def quit_game() -> None:
    global _running
    _running = False


_screen_flags = (pygame.FULLSCREEN | pygame.SCALED)
_running = True
_clock = pygame.time.Clock()
_refresh_rate = 165

InputBinder.register(("keydown", pygame.K_F11),
                     action=lambda: _toggle_tag(pygame.FULLSCREEN))
InputBinder.register(("keydown", pygame.K_END), action=quit_game)
InputBinder.register(("key", pygame.K_LSHIFT), ("keydown", pygame.K_F11),
                     action=lambda: _toggle_tag(pygame.NOFRAME))
