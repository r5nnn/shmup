"""Submodule that controls the execution of the game."""
import os
from typing import Type

import pygame.display

from data.components.input import inputmanager, inputbinder
from data.states.state import State, stateManager


class Control:
    """Class that controls the game."""

    def __init__(self, state_dict: dict[str, Type[State]], start_state: str):
        stateManager.control = self
        stateManager.state_dict = state_dict
        stateManager.append(start_state)

        self.screen = pygame.display.get_surface()
        self.screen_flags = (pygame.FULLSCREEN | pygame.SCALED)

        self.running = True
        self.clock = pygame.time.Clock()
        self.refresh_rate = 165

        inputbinder.register(("keydown", pygame.K_F11),
                                   action=lambda: self._toggle_tag(pygame.FULLSCREEN))
        inputbinder.register(("keydown", pygame.K_END),
                                   action=self.quit)
        inputbinder.register(("keydown", pygame.K_F11), ("key", pygame.K_LSHIFT),
                                   action=lambda: self._toggle_tag(pygame.NOFRAME))

    def update(self):
        """Updates current state, checks for quit requests."""
        if inputmanager.quit:
            self.quit()
        stateManager.current_state.update()
        inputbinder.notify(inputmanager)

    def render(self):
        """Renders current state, ticks the clock and flips the display."""
        stateManager.current_state.render()
        self.clock.tick(self.refresh_rate)
        pygame.display.flip()

    @staticmethod
    def event_loop():
        """Passes events to the event manager."""
        inputmanager.process_events(pygame.event.get())

    def quit(self):
        """Sets running to False."""
        self.running = False

    def main(self):
        """Main loop of the game. Handles events, updates then renders objects."""
        while self.running:
            self.event_loop()
            self.update()
            self.render()

    def _toggle_tag(self, tag):
        self.screen_flags ^= tag
        pygame.display.quit()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
        pygame.display.init()
        pygame.display.set_mode((1920, 1080), self.screen_flags)
        for state in stateManager.state_stack:
            state.screen = pygame.display.get_surface()
