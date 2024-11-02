from typing import Callable, override, Literal

import pygame

from data.core.utils import Singleton, Observer, SingletonABCMeta

input_types = Literal[
    'key', 'keydown', 'keyup',
    'mouse', 'mousedown', 'mouseup',
    'quit'
]


class _InputManager(metaclass=Singleton):
    def __init__(self):
        self._keydown_events = []
        self._keyup_events = []
        self._held_keys = []
        self._mousedown_events = []
        self._mouseup_events = []
        self._mouse_buttons = []
        self._mouse_pos = (0, 0)
        self._quit = False

    @property
    def quit(self):
        return self._quit

    def process_events(self, events: list) -> None:
        self._keydown_events.clear()
        self._keyup_events.clear()
        self._mousedown_events.clear()
        self._mouseup_events.clear()

        for event in events:
            match event.type:
                case pygame.KEYDOWN:
                    self._keydown_events.append(event.key)
                    self._held_keys.append(event.key)
                case pygame.KEYUP:
                    self._keyup_events.append(event.key)
                    self._held_keys.remove(event.key)
                case pygame.MOUSEBUTTONDOWN:
                    self._mousedown_events.append(event.button)
                    self._mouse_buttons.append(event.button)
                case pygame.MOUSEBUTTONUP:
                    self._mouseup_events.append(event.button)
                    self._mouse_buttons.remove(event.button)
                case pygame.QUIT:
                    self._quit = True

        self._mouse_pos = pygame.mouse.get_pos()

    def is_key_down(self, key: int) -> bool:
        return key in self._keydown_events

    def is_key_up(self, key: int) -> bool:
        return key in self._keyup_events

    def is_key_pressed(self, key: int) -> bool:
        return key in self._held_keys

    def is_mouse_down(self, button: int) -> bool:
        return button in self._mousedown_events

    def is_mouse_up(self, button: int) -> bool:
        return button in self._mouseup_events

    def is_mouse_pressed(self, button: int) -> bool:
        return button in self._mouse_buttons

    def get_mouse_pos(self) -> tuple[int, int]:
        return self._mouse_pos


class _InputBinder(Observer, metaclass=SingletonABCMeta):
    def __init__(self, input_manager):
        super().__init__()
        self._input_checks = {
            'key': input_manager.is_key_pressed,
            'keydown': input_manager.is_key_down,
            'keyup': input_manager.is_key_up,
            'mouse': input_manager.is_mouse_pressed,
            'mousedown': input_manager.is_mouse_down,
            'mouseup': input_manager.is_mouse_up,
            'quit': lambda _: input_manager.quit
        }

    @override
    def register(self, *inputs: tuple[input_types, int],
                 action: Callable) -> None:
        self._handlers[inputs] = action

    @override
    def deregister(self, *inputs: tuple[input_types, int]) -> None:
        if inputs in self._handlers:
            self._handlers.pop(inputs)

    @override
    def notify(self) -> None:
        # Sort bindings by priority (more inputs = higher priority)
        sorted_bindings = sorted(self._handlers.items(),
                                 key=lambda binding: len(binding[0]),
                                 reverse=True)
        # Track which inputs have already been used to prevent double execution
        used_inputs = set()

        for inputs, action in sorted_bindings:
            if self._are_inputs_active(inputs, used_inputs):
                action()
                used_inputs.update(inputs)

    def _are_inputs_active(self, inputs, used_inputs):
        for input_type, value in inputs:
            if (input_type, value) in used_inputs:
                return False

            check_func = self._input_checks.get(input_type)
            if check_func and not check_func(value):
                return False
        return True


InputManager = _InputManager()
InputBinder = _InputBinder(InputManager)