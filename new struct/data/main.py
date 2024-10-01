"""Submodule that starts and runs the game.

Does not contain logic, this submodule only starts and facilitates running the game.
Declares the state dictionary with every state in the game, initialises the 
Control class."""
from . import control
from .states import title, options


def main():
    """Runs the game."""
    states = {
        "title": title.Title,
        "options": options.Options
        }
    game = control.Control(states, "title")
    game.main()
