import os

import pygame.display

from .components.events import event_manager, key_manager
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

        event_manager.register(pygame.QUIT, self.quit)
        key_manager.register([pygame.K_END], self.quit)
        key_manager.register([pygame.K_F11],
                             lambda: self._toggle_tag(pygame.FULLSCREEN))
        key_manager.register([pygame.K_LSHIFT, pygame.K_F11],
                             lambda: self._toggle_tag(pygame.NOFRAME))

    @staticmethod
    def update():
        """Updates current state."""
        stateManager.current_state.update()

    def render(self):
        """Renders current state, ticks the clock and flips the display."""
        stateManager.current_state.render()

        self.clock.tick(self.refresh_rate)
        pygame.display.flip()

    @staticmethod
    def event_loop():
        """Passes events to the event manager."""
        for event in pygame.event.get():
            event_manager.notify(event)

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
        pygame.display.set_mode(self.screen.get_size(), self.screen_flags)
        for state in stateManager.states:
            state.screen = pygame.display.get_surface()
