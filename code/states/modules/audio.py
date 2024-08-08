"""Module for creating and managing audio channels and playback."""
import pygame
import os
from pathlib import Path


class Audio:
    _channel_counter = 0  # Class-level counter to assign unique channels

    def __init__(self):
        self.channel_id = Audio._channel_counter
        Audio._channel_counter += 1
        self.channel = pygame.mixer.Channel(self.channel_id)
        self.audio_list = {}
        self.current_audio = None

    def add_audio(self, audio_dir, tag=None) -> None:
        """Load audio from the given path.
        
        Args:
            tag: The name of the audio to associate with the audio directory, if unspecified will use the name of the audio file
            audio_dir: Directory of the audio file.
        """
        if not os.path.isfile(audio_dir):
            raise FileNotFoundError(f"File {audio_dir} does not exist.")
        tag = Path(audio_dir).stem if tag is None else None
        self.audio_list[tag] = pygame.mixer.Sound(audio_dir)

    def play_audio(self, tag, loops=0) -> None:
        """Play the currently loaded music.
        Does nothing if music is already playing. In order to replace music use replace_audio() instead

        Args:
            tag: The name of the audio to play, specified when adding audio.
            loops: Amount of times to loop the audio. -1 for looping indefinately.
        """
        if len(self.audio_list) == 0:
            raise KeyError("No audio loaded to play.")
        if not self.channel.get_busy():
            self.current_audio = None
        if self.current_audio != tag:
            self.channel.play(self.audio_list[tag], loops=loops)
            self.current_audio = tag

    def stop(self):
        """Stop the currently playing audio."""
        self.channel.stop()

    def force_play_audio(self, tag, loops=0) -> None:
        """Overwrite any playing audio and play a new track.

        Args:
            tag: The name of the audio to play, specified when adding audio.
            loops: Amount of times to loop the audio. -1 for looping indefinately.
        """
        if len(self.audio_list) == 0:
            raise KeyError("No audio loaded to play.")
        self.stop()
        self.play_audio(tag=tag, loops=loops)

    def set_volume(self, volume):
        """Set the volume of the audio. Volume should be between 0.0 and 1.0."""
        if not 0.0 <= volume <= 1.0:
            raise ValueError("Volume must be between 0.0 and 1.0.")
        self.channel.set_volume(volume)

    def increase_volume(self, increment=0.1):
        """Increase the volume by a specified increment."""
        current_volume = self.channel.get_volume()
        new_volume = min(1.0, current_volume + increment)
        self.set_volume(new_volume)

    def decrease_volume(self, decrement=0.1):
        """Decrease the volume by a specified decrement."""
        current_volume = self.channel.get_volume()
        new_volume = max(0.0, current_volume - decrement)
        self.set_volume(new_volume)
