from . import State


class Options(State):
    def __init__(self):
        super().__init__()
        print('hi')

    def update_screen(self):
        ...

    def update(self):
        ...

    def render(self):
        super().render()

    def startup(self):
        super().startup()

    def cleanup(self):
        super().cleanup()