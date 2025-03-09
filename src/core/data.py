"""Module for saving and loading game config file."""

import json
from pathlib import Path

import pygame


def save(data: dict, directory: Path) -> None:
    """Save a dictionary to a json file.

    :param data: Dictionary to save.
    :param directory: Directory in which to save file to. If file doesn't
    already exist it is created, otherwise any previous data stored is
    overriden.
    """
    directory.touch()
    with directory.open("w") as file:
        json.dump(data, file, indent=4)


def load(directory: Path, default_config: dict) -> dict:
    """Load a dict from a json file.

    :param directory: The path to the json file.
    :param default_config: The default data of the file. Used if the file
    doesn't exist, is empty or unreadable.
    """
    directory.touch()
    with directory.open() as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            save(default_config, directory)
            return default_config


def validate_config(data: dict, default_config: dict) -> dict:
    """Checks that the format of a config dict matches another.

    :param data: The config dict to validate.
    :param default_config: The format/default data of the config dict.
    :return: A new dict with all invalid/missing data removed/appended.
    """
    if default_config.keys() == data.keys():
        pass
    elif len(default_config) > len(data):
        missing_keys = default_config.keys() - data.keys()
        for key in missing_keys:
            data[key] = default_config[key]
    else:
        invalid_keys = data.keys() - default_config.keys()
        for key in invalid_keys:
            del data[key]
    return data


_default_config = {"flags": {"fullscreen": True, "noframe": True}}
config_dir = Path("config.json")
config = validate_config(load(config_dir, _default_config), _default_config)
# Global data that is lost on game quit.
system_data = {
    "flags": pygame.SCALED,
    "dt": 1.0,
    "quit": False,
    "version": "v0.0.3 prototype",
}
