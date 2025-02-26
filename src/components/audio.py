"""Module containing an audio channel manager class.

Includes instances of all channels to be used in the game.
"""
from __future__ import annotations

import warnings
from functools import wraps
from pathlib import Path

import pygame

from src.core.prepare import audio_paths


def checkaudio(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.no_audio:
            method(self, *args, **kwargs)
    return wrapper


class Audio:
    """Class for managing audio channels.

    When instantiated creates a unique channel associated with the object.
    Audio can then be added and played on that channel. Acts as a wrapper for
    `pygame.mixer.Sound`.
    """

    _channel_counter = 0
    def __init__(self):
        self.channel_id = Audio._channel_counter
        Audio._channel_counter += 1
        try:
            self.channel = pygame.mixer.Channel(self.channel_id)
            self.no_audio = False
        except pygame.error:
            self.no_audio = True
        self.sounds = {}
        self.current_audio = None

    @checkaudio
    def add_audio(self, audio_dir: str, tag: str | None = None) -> None:
        if not Path.is_file(Path(audio_dir)):
            msg = f"File {audio_dir} does not exist."
            raise FileNotFoundError(msg)
        tag = Path(audio_dir).stem if tag is None else None
        self.sounds[tag] = pygame.mixer.Sound(audio_dir)

    @checkaudio
    def play_audio(self, tag: str | None = None, loops: int = 0, *,
                   override: bool = False) -> None:
        if len(self.sounds) > 1 and tag is None:
            warnings.warn("Tag not specified when more than one audio loaded",
                          stacklevel=2)
        tag = next(iter(self.sounds)) if tag is None else tag
        self.stop() if override else None
        if not self.channel.get_busy():
            self.current_audio = None
        if self.current_audio != tag:
            self.channel.play(self.sounds[tag], loops=loops)
            self.current_audio = tag

    @checkaudio
    def stop(self) -> None:
        self.channel.stop()

    @checkaudio
    def set_volume(self, volume: float) -> None:
        if not 0.0 <= volume <= 1.0:
            msg = "Volume must be between 0.0 and 1.0."
            raise ValueError(msg)
        self.channel.set_volume(volume)

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


background_audio = Audio()
background_audio.set_volume(0.2)

button_audio = Audio()
button_audio.set_volume(0.2)
button_audio.add_audio(audio_paths("click"))
