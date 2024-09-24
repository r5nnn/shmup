import pygame

from . import Singleton

class InputManager(metaclass=Singleton):
  def __init__(self):
        self._keydown_events = list()
        self._keyup_events = list()
        self._held_keys = list()
        self._mouse_buttons = list()
        self._mouse_pos = (0, 0)
   
    def process_events(self, events):
        self._keydown_events.clear()
        self._keyup_events.clear()

        for event in events:
            if event.type == pygame.KEYDOWN:
                self._keydown_events.append(event.key)
                self._held_keys.append(event.key)
            elif event.type == pygame.KEYUP:
                self._keyup_events.append(event.key)
                self._held_keys.remove(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_buttons.append(event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._mouse_buttons.remove(event.button)

        self._mouse_pos = pygame.mouse.get_pos()

    def is_key_pressed(self, key):
        return key in self._held_keys

    def is_key_down(self, key):
        return key in self._keydown_events

    def is_key_up(self, key):
        return key in self._keyup_events

    def is_mouse_button_pressed(self, button):
        return button in self._mouse_buttons

    def get_mouse_pos(self):
        return self._mouse_pos
