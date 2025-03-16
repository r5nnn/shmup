"""Module containing an audio channel manager class."""

from __future__ import annotations

import logging
import warnings
from functools import wraps
from pathlib import Path
from typing import Callable, ClassVar, Concatenate, ParamSpec, Self, TypeVar

import pygame


logger = logging.getLogger("src.components.audio")


def checkaudio(method: _Method) -> _Method:
    @wraps(method)
    def wrapper(self: Audio, *args: _P.args, **kwargs: _P.kwargs) -> _Return:
        if not Audio.no_audio:
            method(self, *args, **kwargs)
        else:
            logger.debug(
                "No audio drivers present, ignoring method call attempt: %s.",
                method,
            )

    return wrapper


class _AudioMeta(type):
    """Metaclass to ensure unique Audio instances per channel_id."""

    _instances: ClassVar[dict[str, Audio]] = {}
    channel_counter: int = 0

    def __call__(cls, channel_name: str) -> Audio:
        """Ensure each channel_id has a unique instance."""
        if channel_name in cls._instances:
            return cls._instances[channel_name]  # Return existing instance

        # Create and store new instance
        instance = super().__call__(channel_name)
        cls._instances[channel_name] = instance
        return instance


class Audio(metaclass=_AudioMeta):
    """Class for managing audio channels. Acts as a wrapper for Channel objects.

    When instantiated creates a unique channel associated with the object.
    Audio can then be added and played on that channel. Acts as a wrapper for
    `pygame.mixer.Sound`.
    """

    no_audio = False

    @checkaudio
    def __init__(self, channel_name: str):
        self.channel_name = channel_name
        self.channel_id = _AudioMeta.channel_counter
        _AudioMeta.channel_counter += 1

        try:
            self.channel = pygame.mixer.Channel(self.channel_id)
        except pygame.error:
            logger.exception(
                "Unable to instantiate mixer channels, audio drivers may not "
                "be present. Disabling all audio functionality."
            )
            Audio.no_audio = True
        self.sounds = {}
        self.current_audio = None

    @checkaudio
    def add_audio(self, audio_dir: str, tag: str | None = None) -> None:
        if not Path.is_file(Path(audio_dir)):
            msg = f"File {audio_dir} does not exist."
            raise FileNotFoundError(msg)
        tag = Path(audio_dir).stem if tag is None else None
        if tag in self.sounds:
            warnings.warn(
                f"Attempted to add audio with tag: {tag} already "
                f"used in the sounds dict: {self.sounds}",
                stacklevel=2,
            )
        self.sounds[tag] = pygame.mixer.Sound(audio_dir)
        logger.info(
            "Added audio file %s using tag %s to audio object %s.",
            audio_dir,
            tag,
            repr(self),
        )

    @checkaudio
    def play_audio(
        self, tag: str | None = None, loops: int = 0, *, override: bool = False
    ) -> None:
        if len(self.sounds) > 1 and tag is None:
            warnings.warn(
                "Tag not specified when more than one audio loaded",
                stacklevel=2,
            )
        tag = next(iter(self.sounds)) if tag is None else tag
        self.stop() if override else None
        if not self.channel.get_busy():
            self.current_audio = None
        if self.current_audio != tag:
            self.channel.play(self.sounds[tag], loops=loops)
            self.current_audio = tag
            logger.info(
                "Playing new audio %s in audio object %s. Looping %s times.",
                tag,
                repr(self),
                loops,
            )
        else:
            logger.info(
                "Rejected playing %s audio. Override parameter not set as "
                "True, and audio already playing in channel: %s",
                tag,
                self,
            )

    @checkaudio
    def stop(self) -> None:
        self.channel.stop()

    @checkaudio
    def set_volume(self, volume: float) -> None:
        if not 0.0 <= volume <= 1.0:
            msg = "Volume must be between 0.0 and 1.0."
            raise ValueError(msg)
        self.channel.set_volume(volume)
        logger.info("Set volume of audio object %s as %s", self, volume)

    @checkaudio
    def increase_volume(self, increment: float = 0.1) -> None:
        current_volume = self.channel.get_volume()
        new_volume = min(1.0, current_volume + increment)
        self.set_volume(new_volume)

    @checkaudio
    def decrease_volume(self, decrement: float = 0.1) -> None:
        current_volume = self.channel.get_volume()
        new_volume = max(0.0, current_volume - decrement)
        self.set_volume(new_volume)

    def __repr__(self):
        return f"Audio(channel_name={self.channel_name})"


_P = ParamSpec("_P")
_Return = TypeVar("_Return")
_Method = Callable[Concatenate[Audio, _P], _Return]
