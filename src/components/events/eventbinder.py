"""Used to bind events to actions."""

from __future__ import annotations

import logging
import warnings
from collections import defaultdict
from typing import Callable, TYPE_CHECKING, Any

from src.components.events.utils import (
    is_key_up,
    is_key_down,
    is_key_pressed,
    is_mouse_pressed,
    is_mouse_up,
    is_mouse_down,
)
from src.core.data import system_data

if TYPE_CHECKING:
    from src.core.types import EventTypes

logger = logging.getLogger("src.components.events")

_observers = defaultdict(list)
_input_checks = {
    "key": is_key_pressed,
    "keydown": is_key_down,
    "keyup": is_key_up,
    "mouse": is_mouse_pressed,
    "mousedown": is_mouse_down,
    "mouseup": is_mouse_up,
    "quit": lambda: system_data.quit,
}
_sorted_bindings_cache = None


def register(
    *inputs: tuple[EventTypes, int], action: Callable[[], Any]
) -> None:
    """Registers a combination of inputs to an action."""
    global _sorted_bindings_cache
    _observers[inputs].append(action)
    logger.info(
        "Registered inputs %s to action %s, resetting bindings cache.",
        inputs,
        action,
    )
    _sorted_bindings_cache = None


def deregister(
    *inputs: tuple[EventTypes, int], action: Callable[[], Any] | None = None
) -> None:
    """Deregisters an action from a combination of inputs.

    If blank removes all actions from the combination.
    """
    global _sorted_bindings_cache
    if action is not None and action in _observers[inputs]:
        _observers[inputs].remove(action)
        if not _observers[inputs]:
            _observers.pop(inputs)
            logger.debug(
                "No actions registered to input combination: %s, removing "
                "input combination from dict.",
                inputs,
            )
        logger.info(
            "Deregistered inputs %s from action %s, resetting bindings cache.",
            inputs,
            action,
        )
    elif _observers.pop(inputs, None) is None:
        warnings.warn(
            f"Attempted to deregister inputs {inputs} that haven't "
            f"been registered to the observers dict {_observers}",
            stacklevel=2,
        )
    _sorted_bindings_cache = None


def notify() -> None:
    """Check if registered events have occurred and call observers."""
    _update_sorted_bindings() if _sorted_bindings_cache is None else None
    used_inputs = set()

    for inputs, actions in _sorted_bindings_cache:
        if _are_inputs_active(inputs, used_inputs):
            for action in actions:
                logging.debug(
                    "Inputs: %s detected. Calling action %s.", inputs, action
                )
                action()
            used_inputs.update(inputs)


def is_registered(*events: int, handler: Callable[[], Any]) -> bool:
    """Check if a handler is registered to a combination of events."""
    return events in _observers and handler in _observers[events]


def _update_sorted_bindings() -> None:
    global _sorted_bindings_cache
    _sorted_bindings_cache = sorted(
        _observers.items(), key=lambda binding: len(binding[0]), reverse=True
    )


def _are_inputs_active(
    inputs: tuple[tuple[EventTypes, int]], used_inputs: set
) -> bool:
    for input_type, value in inputs:
        if (input_type, value) in used_inputs:
            return False

        check_func: Callable[[int], Any] | None = _input_checks.get(input_type)
        if check_func is not None and not check_func(value):
            return False
    return True
