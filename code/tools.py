import os

import pygame


class Control:
    def __init__(self):
        self.running = True
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.prev_time = 0
        self.dt_res = 8

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def update(self, dt):
        if self.state.quit:
            self.running = False
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, dt)

    def flip_state(self):
        previous, self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(persist)
        self.state.previous = previous

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.state.get_event(event)

    def get_dt(self):
        """calculates delta time"""
        now = pygame.time.get_ticks() / 1000
        self.dt = round(now - self.prev_time, self.dt_res)
        self.prev_time = now

    def main(self):
        while self.running:
            self.event_loop()
            self.get_dt()
            self.update(self.dt)
            pygame.display.update()


class _State:
    def __init__(self):
        self.previous = None
        self.next = None
        self.persist = {}

    def get_events(self, event):
        pass

    def startup(self, persistant):
        self.persist = persistant

    def cleanup(self):
        return self.persist

    def update(self, surface):
        pass


class Load:
    def __init__(self, directory: str, accept: tuple[str]):
        """
        Loads in files from specified directories.
        Allows for filering accepted files by file extension.


        Args:
            directory: Directory storing all the files to load.
            accept: Tuple of file endings to look for.
        """
        self.files = {}
        for file in os.listdir(directory):
            name, ext = os.path.splitext(file)
            if ext.lower() in accept:
                self.process_file(file, name, directory)

    def process_file(self, file: str, name: str, directory: str):
        """
        Adds the given file to the dictionary.

        Args:
            file: The file to be added to the dictionary.
            name: The name of the file to be used in the dictionary.
            directory: The path where the file is stored.
        """
        self.files[name] = os.path.join(directory, file)

    def __call__(self) -> dict[str, str]:
        """Returns: A dictionary of file names pointing to their directories."""
        return self.files


# class LoadAllGraphics(Load):
#     def __init__(self, directories, accept=(".png", ".jpg", ".jpeg")):
#         """
#         Loads in images
#         Args:
#             directories:
#             accept:
#         """
#         super().__init__(directories, accept)
#
#     @override
#     def process_file(self, file, name, directory):
#         img = pygame.image.load(os.path.join(directory, file))
#         if img.get_alpha():
#             img = img.convert_alpha()
#         else:
#             img = img.convert()
#         self.files[name] = img