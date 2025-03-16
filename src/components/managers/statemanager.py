"""Used to manage states in a state stack."""

from __future__ import annotations

import logging
import warnings
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from src.core.types import AnyState
    from src.states.state import State


logger = logging.getLogger("src.components.managers")
state_dict = {}
state_stack = []


def current_state() -> AnyState:
    """Does what it says.

    :return: The state at the top of the state stack.
    :raises IndexError: If no state in the state stack.
    """
    if state_stack:
        return state_stack[-1]
    msg = (
        f"Attempted to access current state in empty state stack "
        f"{state_stack}."
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
    logger.debug(
        "Attempting to add new state: %s to the state stack %s.",
        state_name,
        state_stack,
    )
    state_stack.append(_initialise_state(state_name))
    current_state().startup()
    logger.info(
        "Appended new state: %s to the state stack %s.",
        state_name,
        state_stack,
    )


def pop() -> None:
    """Removes the state at the top of the state stack."""
    logger.debug(
        "Attempting to remove state %s off the state stack %s.",
        current_state(),
        state_stack,
    )
    current_state().cleanup()
    state_stack.pop()
    current_state().startup()
    logger.info("Popped top state off the state stack %s.", state_stack)


def switch(state_name: str) -> None:
    """Switches out the top state for another one.

    :param state_name: The name of the state in the state dictionary to switch
    to.
    :raises KeyError: If initializing the state fails.
    """
    logger.debug(
        "Attempting to switch state %s for state %s in the state stack %s.",
        current_state(),
        state_name,
        state_stack,
    )
    current_state().clear_widgets()
    current_state().cleanup()
    state_stack.pop()
    state_stack.append(_initialise_state(state_name))
    current_state().startup()
    logger.info(
        "Switched state for state %s in the state stack %s.",
        state_name,
        state_stack,
    )


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
            f"{state_stack!r}",
            stacklevel=2,
        )
        return
    logger.debug(
        "Attempting to go back to state %s in the state stack %s.",
        state_name,
        state_stack,
    )
    current_state().cleanup()
    while current_state() != state_dict[state_name]:
        state_stack.pop()
    current_state().startup()
    logger.debug(
        "Removed all states until reaching state %s in the state stack %s.",
        state_name,
        state_stack,
    )


def quit_game() -> None:
    """Safely quits the game by cleaning up processes in the current state.

    Posts a `pygame.QUIT` event in the event stack.
    """
    if current_state():
        current_state().cleanup()
    pygame.event.post(pygame.event.Event(pygame.QUIT))
    logger.info(
        "Called quit_game method, exiting current state %s and posting "
        "pygame.QUIT event in the event stack.",
        current_state(),
    )
