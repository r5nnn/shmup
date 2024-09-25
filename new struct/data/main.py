from . import control
from .states import title

def main():
    states = {
        "title": title.Title
    }
    game = control.Control(states, "title")
    game.main()
