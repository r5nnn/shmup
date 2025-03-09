"""Used to manage states in a state stack."""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from src.core.types import AnyState
    from src.states.state import State


state_dict = {}
_state_stack = []


def current_state() -> AnyState:
    """Does what it says.

    :return: The state at the top of the state stack.
    :raises IndexError: If no state in the state stack.
    """
    if _state_stack:
        return _state_stack[-1]
    msg = (
        f"Attempted to access current state in empty state stack "
        f"{_state_stack}."
    )
    raise IndexError(msg)


def _validate(state_name: str) -> bool:
    return not state_name.lower() not in state_dict


def _initialise_state(state_name: str) -> State:
    if _validate(state_name):
        state_class = state_dict[state_name.lower()]
        return state_class()
    msg = (
        f"Initializing state {state_name!r} failed. State does not exist in"
        f" state dictionary {state_dict!r}."
    )
    raise KeyError(msg)


def append(state_name: str, *, initial: bool = False) -> None:
    """Adds a new state to the top of the state stack.

    :param state_name: The name of the state in the state dictionary to add.
    :param initial: Should be set to True if the state being added is the first
    state. Defaults to False
    :raises KeyError: If initializing the state fails.
    """
    if not initial:
        current_state().cleanup()
    _state_stack.append(_initialise_state(state_name))
    current_state().startup()


def pop() -> None:
    """Removes the state at the top of the state stack."""
    current_state().cleanup()
    _state_stack.pop()
    current_state().startup()


def switch(state_name: str) -> None:
    """Switches out the top state for another one.

    :param state_name: The name of the state in the state dictionary to switch
    to.
    :raises KeyError: If initializing the state fails.
    """
    current_state().clear_widgets()
    current_state().cleanup()
    _state_stack.pop()
    _state_stack.append(_initialise_state(state_name))
    current_state().startup()


def back_to(state_name: str) -> None:
    """Removes states from the top of the state stack until the state specified.

    :param state_name: The name of the state already in the state stack to go
    back to.
    """
    if not _validate(state_name):
        warnings.warn(
            f"Attempted to go back to state {state_name!r} that "
            f"doesn't exist in the state dictionary: {state_dict!r}",
            stacklevel=2,
        )
        return
    if current_state() == state_dict[state_name]:
        warnings.warn(
            f"Attempted to go back to state {state_name!r} that was"
            f"already the current state in the state stack "
            f"{_state_stack!r}",
            stacklevel=2,
        )
        return
    current_state().cleanup()
    while current_state() != state_dict[state_name]:
        _state_stack.pop()
    current_state().startup()


def quit_game() -> None:
    """Safely quits the game by cleaning up processes in the current state.

    Posts a `pygame.QUIT` event in the event stack.
    """
    if current_state():
        current_state().cleanup()
    pygame.event.post(pygame.event.Event(pygame.QUIT))
