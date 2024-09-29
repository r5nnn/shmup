import warnings

import pygame
import os
from pathlib import Path

from data import audio_paths


class Audio:
    _channel_counter = 0  # Class-level counter to assign unique channels

    def __init__(self):
        """
        Class for creating and managing pygame channel and sound objects.
        Keeps track of channels used, assigns new
        channel each time class is called.
        Allows for loading up multiple audio files for a channel,
        which avoids the lag of loading files repeatedly.
        Also allows for ignoring repeat requests to
        play a song that is already playing.

        Examples:
            a = Audio()
            a.add_audio(audio1_file_path)
            a.add_audio(audio2_file_path)
            a.play_audio('audio1', loops=-1)
            a.play_audio('audio1') # does nothing since audio already playing
            a.play_audio('audio1', override=True) # replays audio1 regardless
        """
        self.channel_id = Audio._channel_counter
        Audio._channel_counter += 1
        self.channel = pygame.mixer.Channel(self.channel_id)
        self.audio_list = {}
        self.current_audio = None

    def add_audio(self, audio_dir: str, tag: str = None) -> None:
        """
        Load audio from the given path.

        Args:
            tag: The name of the audio to associate with the audio directory,
            if unspecified will use the name of the audio file.
            audio_dir: Directory of the audio file.
        """
        if not os.path.isfile(audio_dir):
            raise FileNotFoundError(f"File {audio_dir} does not exist.")
        tag = Path(audio_dir).stem if tag is None else None
        self.audio_list[tag] = pygame.mixer.Sound(audio_dir)

    def play_audio(self, tag: str = None, loops: int = 0,
                   override: bool = False) -> None:
        """
        Plays the audio of the tag specified.
        Does nothing if the same audio file is already playing.

        Args:
            tag: The name of the audio to play, specified when using add_audio.
            Can be left unspecified if only one audio is loaded into the class.
            loops: Amount of times to loop the audio, -1 for looping
            indefinately.
            override: Whether the audio should play even if the currently
            playing audio is equal to the audio being requested to play.
        """
        if len(self.audio_list) == 0:
            raise KeyError("No audio loaded to play.")
        elif len(self.audio_list) > 1 and tag is None:
            warnings.warn("Tag not specified when more than one audio loaded")
        if loops < -1:
            raise ValueError("loops argument cannot be smaller than -1.")

        # set tag to first sound object if unspecified
        tag = self.audio_list[0] if tag is None else tag
        # force stop the currently playing audio if override is True
        self.stop() if override else None
        if not self.channel.get_busy():
            self.current_audio = None
        if self.current_audio != tag:
            self.channel.play(self.audio_list[tag], loops=loops)
            self.current_audio = tag

    def stop(self):
        """Stop the currently playing audio."""
        self.channel.stop()

    def set_volume(self, volume: float):
        """Set the volume of the audio. Volume should be between 0.0 and 1.0.
        """
        if not 0.0 <= volume <= 1.0:
            raise ValueError("Volume must be between 0.0 and 1.0.")
        self.channel.set_volume(volume)

    def increase_volume(self, increment: float = 0.1):
        """Increase the volume by a specified increment."""
        current_volume = self.channel.get_volume()
        # makes sure volume doesn't increase above 1.0
        new_volume = min(1.0, current_volume + increment)
        self.set_volume(new_volume)

    def decrease_volume(self, decrement: float = 0.1):
        """Decrease the volume by a specified decrement."""
        current_volume = self.channel.get_volume()
        # makes sure volume doesn't decrease below 0
        new_volume = max(0.0, current_volume - decrement)
        self.set_volume(new_volume)

background_audio = Audio()
background_audio.set_volume(0.2)
button_audio = Audio()
button_audio.set_volume(0.2)

button_audio.add_audio(audio_paths('click'))