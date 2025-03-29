"""Contains base classes for both states and overlays."""

from __future__ import annotations

from typing import override, TYPE_CHECKING

import pygame

from src.components.managers import statemanager, overlaymanager
from src.components.ui import widgethandler
from src.core.data import system_data

if TYPE_CHECKING:
    from src.components.ui.widgetutils import WidgetBase


class Overlay:
    background: None | pygame.Surface
    widgets: list[WidgetBase]

    def __init__(self):
        """Base class for making overlays.

        Overlays have their own dedicated overlay stack, independent from the
        state stack. This functions differently than the state stack: an
        overlay does not need to exist for the game to run and when a new
        overlay is appended on top of another overlay, the overlay below it is
        not cleaned up. An overlay is only cleaned up when it is actually
        removed from the overlay stack.

        Just like states, overlays have their own widgets list, however when
        no background is specified, instead of rendering a black screen like
        states, it just doesn't render anything.

        A back function exists for overlays, though it is not bound to any
        global keybind like escape is for states.

        It also doesn't update the widgethandler, since that is handled by the
        current state.
        """
        self.background = None
        self.widgets = []

    def startup(self) -> None:
        """Method called whenever the overlay added to the overlay stack.

        This should usually not be overriden, as any logic that is placed under
        this method could be placed under __init__, since this method is ONLY
        called once, when the overlay is appended to overlay stack unlike
        states, where appending another state on top of another one exits the
        previous state.

        This method still exists to ensure that the self.widgets list can be
        defined, while all the widgets added after calling super().__init__()
        can still be added.
        """
        widgethandler.add_widget(*self.widgets)

    def cleanup(self) -> None:
        """Method called whenever the overlay is removed from the overlay stack.

        Automatically removes all the widgets in the self.widgets list from the
        widgethandler.
        """
        widgethandler.remove_widget(*self.widgets)

    def update(self) -> None:
        """Updates all the features of the overlay before rendering."""

    def render(self) -> None:
        """Renders the overlay onto the screen."""

    def back(self) -> None:
        """Removes the top overlay from the overlay stack."""
        overlaymanager.pop()

    @override
    def __str__(self):
        return (
            f"<{self.__class__.__name__} self.widgets="
            f"{[widget.__class__.__name__ for widget in self.widgets]}>"
        )


class State(Overlay):
    def __init__(self):
        """Base class for making states.

        States are ordered in a state stack using a dedicated state manager.
        Only the state at the top of the stack is updated and rendered, though
        this can be worked around by having the top state call another state's
        update and render methods whenever it itself updates and renders. At
        least one state is required to be present in the state stack at all
        times for the game to run.

        States have their own widgets list which contains every widget of that
        state. These are automatically added and removed from the widgethandler
        when the state is entered/exited.

        widgethandler.update() and blit() is called every frame in the update
        and render methods by default.

        If the background property remains undefined, it is automatically
        assigned to a black surface the size of the screen. This background (or
        any other defined background) is rendered onto the screen every frame.
        """
        super().__init__()
        if len(statemanager.state_stack) >= 1:
            self.background = statemanager.current_state().background
        else:
            self.background = pygame.Surface(system_data.abs_window_rect.size)

    @override
    def startup(self) -> None:
        """Method called whenever the state becomes the top state.

        This could be by being directly placed at the top of the state stack,
        or by a state above this state being removed, making this state the
        top state.

        Adds all the widgets from the self.widgets list to the widgethandler.
        """
        super().startup()

    @override
    def cleanup(self) -> None:
        """Method called whenever the state is no longer the top state.

        This could be by being removed from the state stack entirely, or by
        another state being added on top of this one.

        Automatically removes all the widgets in the self.widgets list from the
        widgethandler.
        """
        super().cleanup()

    @override
    def update(self) -> None:
        """Updates all the features of the state before rendering.

        Updates all of the widgets by calling widgethandler.update()
        """
        widgethandler.update()

    @override
    def render(self) -> None:
        """Renders the state onto the screen."""
        system_data.abs_window.blit(self.background, (0, 0))

    @override
    def back(self) -> None:
        """Pops the top state off of the state stack."""
        statemanager.pop()
