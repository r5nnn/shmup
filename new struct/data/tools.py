import pygame.display

from .components.events import generalEventManager, keyManager
from .globals import MONITOR_SIZE, screen, display

from .components import pygame_shaders


class Control:
    def __init__(self, state_dict, start_state):
        self.state_stack = []
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.state_stack.append(self.state_name)

        self.screen = screen
        self.display = display
        self.screen_shader = pygame_shaders.DefaultScreenShader(self.display)
        self.screen_rect = self.screen.get_rect()
        self.screen_size = self.screen.get_size()
        self.screen_flags = (pygame.SCALED | pygame.FULLSCREEN |
                             pygame.OPENGL | pygame.DOUBLEBUF)

        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = 144
        generalEventManager.register(pygame.QUIT, self.quit)
        keyManager.register([pygame.K_END], self.quit)
        keyManager.register([pygame.K_F11],
                            lambda: self._toggle_tag(pygame.FULLSCREEN))
        keyManager.register([pygame.K_LSHIFT, pygame.K_F11],
                            lambda: self._toggle_tag(pygame.NOFRAME))

    def update(self):
        self.state_dict[self.state_stack[-1]].update()

    def render(self):
        self.state_dict[self.state_stack[-1]].render()
        self.screen_shader.render()

        self.clock.tick(self.fps)
        pygame.display.flip()

    @staticmethod
    def event_loop():
        for event in pygame.event.get():
            generalEventManager.notify(event)

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.state_stack.append(self.state_name)

    def quit(self):
        self.running = False

    def main(self):
        while self.running:
            self.event_loop()
            self.update()
            self.render()

    def _toggle_tag(self, tag):
        self.screen_flags ^= tag
        pygame.display.set_mode(self.screen_size, self.screen_flags)


class State:

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.display = display
        self.background = pygame.Surface(MONITOR_SIZE)
        self.surfaces = []

    def update(self, *args):
        pass

    def render(self):
        self.display.blit(self.background, (0, 0))
        for surface, coords in self.surfaces:
            self.display.blit(surface, coords)