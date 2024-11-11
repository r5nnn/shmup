"""Module that initialises the game loop with all the game's states."""
from data.core import control
from data.states import title, options, game


def main():
    states = {"title": title.Title, "options": options.Options, "game": game.Game}
    control.initialise(states, "title")
    control.main()
