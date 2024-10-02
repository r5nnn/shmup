"""Module for initiating and handling the playback of audio from audio files."""
import warnings

import pygame
import os
from pathlib import Path

from data.core.prepare import audio_paths


class Audio:
    """Class for creating and managing pygame channel and sound objects.
    Keeps track of channels used, assigns new channel each time class is called."""
    _channel_counter = 0  # Class-level counter to assign unique channels to each new instance

    def __init__(self):
        self.channel_id = Audio._channel_counter
        Audio._channel_counter += 1
        self.channel = pygame.mixer.Channel(self.channel_id)
        self.audio_list = {}
        self.current_audio = None

    def add_audio(self, audio_dir: str, tag: str = None) -> None:
        """Load audio from the given path

        :param audio_dir: Directory of the audio file to add.
        :param tag: The name of the audio to associate with the sound object,
            defaults to None, in which case the filename will be used as the tag."""
        if not os.path.isfile(audio_dir):
            raise FileNotFoundError(f"File {audio_dir} does not exist.")
        tag = Path(audio_dir).stem if tag is None else None
        self.audio_list[tag] = pygame.mixer.Sound(audio_dir)

    def play_audio(self, tag: str = None, loops: int = 0, override: bool = False) -> None:
        """Plays the audio of the tag specified if the channel is not busy.

        :param tag: The name of the audio to play, defaults to None which will
            use the first audio file added to that channel (this should only
            be used if there is only one audio file loaded for clarity).
        :param loops: Amount of times to loop the audio, -1 loops indefinately.
        :param override: Whether the audio should play even if the channel is
            busy. The previously playing audio will stop.

        :raises KeyError: If no audio has been added to the channel.
        :raises ValueError: If the loops argument is smaller than -1."""
        if len(self.audio_list) == 0:
            raise KeyError("No audio loaded to play.")
        elif len(self.audio_list) > 1 and tag is None:
            warnings.warn("Tag not specified when more than one audio loaded")
        if loops < -1:
            raise ValueError("loops argument cannot be smaller than -1.")

        tag = self.audio_list[0] if tag is None else tag
        self.stop() if override else None
        if not self.channel.get_busy():
            self.current_audio = None
        if self.current_audio != tag:
            self.channel.play(self.audio_list[tag], loops=loops)
            self.current_audio = tag

    def stop(self) -> None:
        """Stop the currently playing audio."""
        self.channel.stop()

    def set_volume(self, volume: float) -> None:
        """Set the volume of the audio.
        
        :param volume: The volume to set the channel to.
        :raises ValueError: If the volume is not between 0.0 or 1.0"""
        if not 0.0 <= volume <= 1.0:
            raise ValueError("Volume must be between 0.0 and 1.0.")
        self.channel.set_volume(volume)

    def increase_volume(self, increment: float = 0.1) -> None:
        """Increase the volume by a specified increment.
        
        :param increment: The amount to increase the volume by."""
        current_volume = self.channel.get_volume()
        # makes sure volume doesn't increase above 1.0
        new_volume = min(1.0, current_volume + increment)
        self.set_volume(new_volume)

    def decrease_volume(self, decrement: float = 0.1) -> None:
        """Decrease the volume by a specified decrement.
        
        :param decrement: The amount to decrease the volume by."""
        current_volume = self.channel.get_volume()
        # makes sure volume doesn't decrease below 0
        new_volume = max(0.0, current_volume - decrement)
        self.set_volume(new_volume)


background_audio = Audio()
background_audio.set_volume(0.2)
button_audio = Audio()
button_audio.set_volume(0.2)

button_audio.add_audio(audio_paths('click'))
