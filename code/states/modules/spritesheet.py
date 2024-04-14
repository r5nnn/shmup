"""Module that allows for parsing spritesheets in order to load in specific sprites."""
import sys
import json
import pygame


class Spritesheet:
    def __init__(self, spritesheet_dir: str):
        """Initialises Spritesheet, creates the spritesheet surface, and reads associated json file

        Args: spritesheet_dir: Directory to spritesheet, without file ending. Spritesheet image should end .png while associated json file should have the
        same name
        """
        # load in entire spritesheet surface
        self.spritesheet = pygame.image.load(spritesheet_dir + '.png').convert_alpha()
        # load in json data of spritesheet
        self.metadata = spritesheet_dir + '.json'

        # error handling
        try:
            metadata_json = open(self.metadata, encoding='UTF-8')
        except OSError:
            print('Could not open/read file:', self.metadata)
            sys.exit()
        with metadata_json:
            self.data = json.load(metadata_json)  # extracts json data as python dicts
        metadata_json.close()

    def _get_sprite(self, x: int, y: int, width: int, height: int) -> pygame.Surface:
        """Returns subsurface from spritesheet of coordinates specified.

        This method is not meant to be called explicitly, rather call Spritesheet.parse_sprite for the sprite surface.

        Args:
            x: Topleft x coordinate of image to cut out.
            y: Topleft y coordinate of image to cut out.
            width: Width of image to cut out.
            height: Height of image to cut out.

        Returns: surface from spritesheet of coordinates specified.
        """
        return self.spritesheet.subsurface(x, y, width, height)

    def parse_sprite(self, name: str) -> pygame.Surface:
        """Parses sprite coordinates from name of sprite given.

        Json file must include the name of each sprite with their respective x, y, width and height attributes.

        Args:
            name: Name of sprite as listed in spritesheet json file.

        Returns: surface including sprite specified.
        """
        sprite = self.data['frames'][name]['frame']
        return self._get_sprite(sprite['x'], sprite['y'], sprite['w'], sprite['h'])
