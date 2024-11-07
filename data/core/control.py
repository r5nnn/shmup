from typing import Type

import pygame.display

import data.core.utils
from data.components.input import InputManager, InputBinder
from data.states.state import State, state_manager


class Control:
    def __init__(self, state_dict: dict[str, Type[State]], start_state: str):
        state_manager.control = self
        state_manager.state_dict = state_dict
        state_manager.append(start_state)

        self.screen = pygame.display.get_surface()
        self.screen_flags = (pygame.FULLSCREEN | pygame.SCALED)

        self.running = True
        self.clock = pygame.time.Clock()
        self.refresh_rate = 165

        InputBinder.register(("keydown", pygame.K_F11), action=lambda:
        self._toggle_tag(pygame.FULLSCREEN))
        InputBinder.register(("keydown", pygame.K_END), action=self.quit)
        InputBinder.register(("key", pygame.K_LSHIFT),
                             ("keydown", pygame.K_F11),
                             action=lambda: self._toggle_tag(pygame.NOFRAME))

    def update(self):
        if InputManager.quit:
            self.quit()
        InputBinder.notify()
        state_manager.current_state.update()

    def render(self):
        state_manager.current_state.render()
        data.core.utils.dt = self.clock.tick(self.refresh_rate) / 1000.0
        pygame.display.flip()

    @staticmethod
    def event_loop():
        InputManager.process_events(pygame.event.get())

    def quit(self):
        """Sets running to False."""
        self.running = False

    def main(self):
        while self.running:
            self.event_loop()
            self.update()
            self.render()

    def _toggle_tag(self, tag):
        self.screen_flags ^= tag
        pygame.display.set_mode((1920, 1080), self.screen_flags)
