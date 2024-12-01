"""Module for initialising the game loop with all the game's states."""
from data.core import control
from data.states import game, options, title


def main() -> None:
    states = {"title": title.Title, "options": options.Options, "game": game.Game}
    control.initialise(states, "title")
    control.main()
