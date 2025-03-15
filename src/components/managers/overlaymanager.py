"""Used to manage overlays in an overlay stack."""

from __future__ import annotations

import logging
import warnings
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.states.state import Overlay


logger = logging.getLogger("src.components.managers")
overlay_stack = []


def current_overlay(*, accept_no_overlay: bool = False) -> Overlay | None:
    """Does what it says.

    :param accept_no_overlay: Should an error be raised if no overlay present
    in the overlay stack. Defaults to False.
    :return: The overlay at the top of the overlay stack, or None if the stack
    is empty and `accept_no_overlay` is True.
    :raises IndexError: If `accept_no_overlay` is False and no overlay in the
    overlay stack.
    """
    if overlay_stack:
        return overlay_stack[-1]
    if accept_no_overlay:
        return None
    msg = (
        f"Attempted to access current overlay when `accept_no_overlay` was"
        f"False, and overlay stack {overlay_stack} is empty."
    )
    raise IndexError(msg)


def append(overlay: type[Overlay]) -> None:
    """Adds an overlay to the top of the overlay stack.

    :param overlay: The overlay to add.
    """
    logger.debug(
        "Attempting to add new overlay: %s to the overlay stack %s.",
        overlay,
        overlay_stack,
    )
    overlay_stack.append(overlay())
    current_overlay().startup()
    logger.info(
        "Appended new overlay: %s to the overlay stack %s.",
        overlay,
        overlay_stack,
    )


def pop() -> None:
    """Removes the overlay at the top of the overlay stack."""
    logger.debug(
        "Attempting to pop top overlay off the overlay stack: %s.",
        overlay_stack,
    )
    current_overlay().cleanup()
    overlay_stack.pop()
    logger.info("Popped top overlay off the overlay stack: %s.", overlay_stack)


def remove(overlay: type[Overlay]) -> bool:
    """Removes a specific overlay from the overlay stack.

    :param overlay: The overlay to remove.
    :return: True if overlay was successfully removed and False if it was not
    found in the stack.
    """
    for obj in overlay_stack:
        if isinstance(obj, overlay):
            logger.debug(
                "Attempting to remove overlay: %s from overlay stack %s.",
                overlay,
                overlay_stack,
            )
            obj.cleanup()
            overlay_stack.remove(obj)
            logger.info(
                "Removed overlay: %s from the overlay stack %s.",
                overlay,
                overlay_stack,
            )
            return True
    warnings.warn(
        f"Attempted to remove overlay {overlay} which was not "
        f"present in the overlay stack {overlay_stack}.",
        stacklevel=2,
    )
    return False
