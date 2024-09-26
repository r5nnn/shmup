import os

import pygame.display

from .components.events import event_manager, key_manager
from .components.input import InputManager, InputBinder
from .states import stateManager


class Control:
    """Class that controls the game."""

    def __init__(self, state_dict, start_state):
        """Adds dictionary to stateManager and defines starting state.
        Initialises game properties, binds global keybinds.
        """
        stateManager.control = self
        stateManager.state_dict = state_dict
        stateManager.append(start_state)

        self.screen = pygame.display.get_surface()
        self.screen_flags = (pygame.FULLSCREEN | pygame.SCALED)

        self.running = True
        self.clock = pygame.time.Clock()
        self.refresh_rate = 165

        self.input_manager = InputManager()
        self.input_binder = InputBinder()

        self.input_binder.bind(("key", pygame.K_END), action=self.quit)
        self.input_binder.bind(("key", pygame.K_F11),
                               action=lambda:
                               self._toggle_tag(pygame.FULLSCREEN))
        # key_manager.register([pygame.K_LSHIFT, pygame.K_F11],
        #                      lambda: self._toggle_tag(pygame.NOFRAME))

    def update(self):
        """Updates current state."""
        stateManager.current_state.update()
        self.input_binder.process_bindings(self.input_manager)

    def render(self):
        """Renders current state, ticks the clock and flips the display."""
        stateManager.current_state.render()

        self.clock.tick(self.refresh_rate)
        pygame.display.flip()

    def event_loop(self):
        """Passes events to the event manager."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            self.input_manager.process_events(event)

    def quit(self):
        """Sets running to False."""
        self.running = False

    def main(self):
        """The main loop of the game. Handles events, updates then renders
        objects."""
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