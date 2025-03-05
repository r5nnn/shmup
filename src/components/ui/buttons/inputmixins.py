from __future__ import annotations

from typing import Callable, ParamSpec, TypeVar, Concatenate

from src.components import button_audio, events
from src.core.constants import LEFTCLICK


class ButtonMixinFields:
    # Defined when integrated with a button class.
    audio_tags: list[str | None] | None = ...
    contains: Callable[[int, int], bool] = ...


class ClickInputMixin(ButtonMixinFields):
    def __init__(self, on_click: Callable | None = None,
                 on_release: Callable | None = None):
        self.on_click_call = on_click
        self.on_release_call = on_release
        self.clicked = False

    def update_click(self) -> None:
        self.clicked = True
        if self.audio_tags[0] is not None:
            button_audio.play_audio(self.audio_tags[0], override=True)

    def update_release(self) -> None:
        """Method that is called when the buttons is released."""
        self.clicked = False
        if self.audio_tags[2] is not None:
            button_audio.play_audio(self.audio_tags[2], override=True)

    def update_hover(self) -> None:
        """Method that is called when the buttons is hovered."""
        if self.audio_tags[1] is not None:
            button_audio.play_audio(self.audio_tags[1], override=True)

    def update_idle(self) -> None:
        """Method that is called when the buttons is idle."""
        self.clicked = False

    def update(self) -> None:
        x, y = events.get_mouse_pos()
        if self.contains(x, y):
            # released
            if events.is_mouse_up(LEFTCLICK) and self.clicked:
                self.update_release()
                self.on_release_call() if self.on_release_call is not None else None
            # clicked
            elif events.is_mouse_down(LEFTCLICK):
                self.update_click()
                if self.on_click_call is not None:
                    self.clicked = False
                    self.on_click_call()
            # hovered
            elif not self.clicked:
                self.update_hover()
        # not interacted with
        else:
            self.update_idle()


class ToggleInputMixin(ButtonMixinFields):
    def __init__(self, on_toggle_on: Callable | None = None,
                 on_toggle_off: Callable | None = None, *,
                 requires_state: bool = False):
        self.on_toggle_off = on_toggle_off
        self.on_toggle_on = on_toggle_on
        self.requires_state = requires_state
        self.toggled = False
        self.sub_widget = False

    def toggle_on(self) -> None:
        """Turn the toggle state on."""
        self.toggled = True

    def toggle_on_call(self, *, silent: bool = False) -> None:
        self.toggle_on()
        if not silent and self.audio_tags[0] is not None:
            button_audio.play_audio(self.audio_tags[0], override=True)
        if self.on_toggle_on is not None:
            self.on_toggle_on(True) if self.requires_state else (
                self.on_toggle_on())

    def toggle_off(self) -> None:
        """Turn the toggle state off."""
        self.toggled = False
        # no need to toggle colors off since that is handled by update hover and idle

    def toggle_off_call(self, *, silent: bool = False) -> None:
        self.toggle_off()
        if not silent and self.audio_tags[2] is not None:
            button_audio.play_audio(self.audio_tags[2], override=True)
        if self.on_toggle_off is not None:
            self.on_toggle_off(False) if self.requires_state else (
                self.on_toggle_off())

    def update_hover(self) -> None:
        if self.audio_tags[1] is not None:
            button_audio.play_audio(self.audio_tags[1], override=True)

    def update_idle(self) -> None:
        ...

    def update(self) -> None:
        x, y = events.get_mouse_pos()
        if self.contains(x, y):
            # toggled on
            if events.is_mouse_down(LEFTCLICK) and not self.toggled:
                self.toggle_on_call()
            # toggled off
            elif (not self.sub_widget and
                  events.is_mouse_down(LEFTCLICK) and self.toggled):
                self.toggle_off_call()
            # hovered
            elif not self.toggled:
                self.update_hover()
        else:
            # not interacted with
            self.update_idle()


def checktoggle(method: _Method) -> _Method:
    def wrapper(self: ToggleInputMixin, *args: _P.args,
                **kwargs: _P.kwargs) -> _Return:
        if not self.toggled:
            method(self, *args, **kwargs)
    return wrapper


_P = ParamSpec("_P")
_Return = TypeVar("_Return")
_Method = Callable[Concatenate[ToggleInputMixin, _P], _Return]
