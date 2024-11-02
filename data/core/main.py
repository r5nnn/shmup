from data.core import control
from data.states import title, options, game


def main():
    states = {
        "title": title.Title,
        "options": options.Options,
        'game': game.Game,
    }
    shmup = control.Control(states, "title")
    shmup.main()
