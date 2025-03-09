"""Used to manage overlays in an overlay stack."""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.states.state import Overlay


_overlay_stack = []


def current_overlay(*, accept_no_overlay: bool = False) -> Overlay | None:
    """Does what it says.

    :param accept_no_overlay: Should an error be raised if no overlay present
    in the overlay stack. Defaults to False.
    :return: The overlay at the top of the overlay stack, or None if the stack
    is empty and `accept_no_overlay` is True.
    :raises IndexError: If `accept_no_overlay` is False and no overlay in the
    overlay stack.
    """
    if _overlay_stack:
        return _overlay_stack[-1]
    if accept_no_overlay:
        return None
    msg = (
        f"Attempted to access current overlay when `accept_no_overlay` was"
        f"False, and overlay stack {_overlay_stack} is empty."
    )
    raise IndexError(msg)


def append(overlay: type[Overlay]) -> None:
    """Adds an overlay to the top of the overlay stack.

    :param overlay: The overlay to add.
    """
    _overlay_stack.append(overlay())
    current_overlay().startup()


def pop() -> None:
    """Removes the overlay at the top of the overlay stack."""
    current_overlay().cleanup()
    _overlay_stack.pop()


def remove(overlay: type[Overlay]) -> bool:
    """Removes a specific overlay from the overlay stack.

    :param overlay: The overlay to remove.
    :return: True if overlay was successfully removed and False if it was not
    found in the stack.
    """
    for obj in _overlay_stack:
        if isinstance(obj, overlay):
            obj.cleanup()
            _overlay_stack.remove(obj)
            return True
    warnings.warn(
        f"Attempted to remove overlay {overlay} which was not "
        f"present in the overlay stack {_overlay_stack}.",
        stacklevel=2,
    )
    return False
