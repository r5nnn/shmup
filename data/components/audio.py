"""Module containing audio channel manager class and module level 
global instances of all channels to be used in the game."""
import warnings
from typing import Optional

import pygame
import os
from pathlib import Path

from data.core.prepare import audio_paths


class Audio:
    _channel_counter = 0

    def __init__(self):
        self.channel_id = Audio._channel_counter
        Audio._channel_counter += 1
        self.channel = pygame.mixer.Channel(
            self.channel_id)
        self.sounds = {}
        self.current_audio = None

    def add_audio(self, audio_dir: str, tag: Optional[str] = None) -> None:
        if not os.path.isfile(audio_dir):
            raise FileNotFoundError(f"File {audio_dir} does not exist.")
        tag = Path(audio_dir).stem if tag is None else None
        self.sounds[tag] = pygame.mixer.Sound(audio_dir)

    def play_audio(self, tag: str = None, loops: int = 0,
                   override: bool = False) -> None:
        if len(self.sounds) == 0:
            raise KeyError("No audio loaded to play.")
        elif len(self.sounds) > 1 and tag is None:
            warnings.warn("Tag not specified when more than one audio loaded")
        if loops < -1:
            raise ValueError("loops argument cannot be smaller than -1.")
        tag = next(iter(self.sounds)) if tag is None else tag
        self.stop() if override else None
        if not self.channel.get_busy():
            self.current_audio = None
        if self.current_audio != tag:
            self.channel.play(self.sounds[tag], loops=loops)
            self.current_audio = tag

    def stop(self) -> None:
        self.channel.stop()

    def set_volume(self, volume: float) -> None:
        if not 0.0 <= volume <= 1.0:
            raise ValueError("Volume must be between 0.0 and 1.0.")
        self.channel.set_volume(volume)

    def increase_volume(self, increment: float = 0.1) -> None:
        current_volume = self.channel.get_volume()
        new_volume = min(1.0, current_volume + increment)
        self.set_volume(new_volume)

    def decrease_volume(self, decrement: float = 0.1) -> None:
        current_volume = self.channel.get_volume()
        new_volume = max(0.0, current_volume - decrement)
        self.set_volume(new_volume)


background_audio = Audio()
background_audio.set_volume(0.2)

button_audio = Audio()
button_audio.set_volume(0.2)
button_audio.add_audio(audio_paths('click'))
