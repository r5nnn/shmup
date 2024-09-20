from . import tools, globals
from .states import title


def main():
    state_dict = {
        "Title": title.Title()
    }
    run = tools.Control(state_dict, "Title")
    run.main()
