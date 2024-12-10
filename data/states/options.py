import pygame

from data.components.ui import ToggleGroup, widgethandler, \
    ToggleableTextButton, ToggleableTextButtonConfig, Text
from data.core import Colors
from data.core.prepare import image_paths, screen, screen_size, screen_center
from data.states.state import State


class Options(State):
    def __init__(self):
        super().__init__()
        self.background = pygame.image.load(image_paths("menu")).convert()
        self.title = pygame.transform.scale_by(
            pygame.image.load(image_paths("title options")), 4)
        self.bg_rect = pygame.Rect(0, screen_size[1] * 0.1 + 20 + self.title.get_height(),
                                   screen_size[0] * 0.8, (screen_size[1] - self.title.get_height()) * 0.8)
        self.bg_rect.centerx = screen_center[0]
        self.bg_surf = pygame.Surface(self.bg_rect.size)
        self.bg_surf.fill(Colors.PRIMARY)
        self.bg_surf.set_alpha(96)
        self.current_option = None
        config = ToggleableTextButtonConfig(position=self.bg_rect.topleft,
                                            size=(round(self.bg_rect.width / 3), 30),
                                            colors=(Colors.PRIMARY,
                                                    Colors.SECONDARY,
                                                    Colors.ACCENT),
                                            text="Graphics")
        self.graphics = ToggleableTextButton(config)
        config.position = self.graphics.rect.topright
        config.text = "Keybinds"
        self.keybinds = ToggleableTextButton(config)
        config.position = self.keybinds.rect.topright
        config.text = "Audio"
        self.audio = ToggleableTextButton(config)
        self.options = ToggleGroup(self.graphics, self.audio, self.keybinds)
        widgethandler.add_widget(self.graphics, self.audio, self.keybinds)
        self._padding = 20
        fullscreen_text = Text((self.bg_rect.left + self._padding, self.bg_rect.top + self.graphics.height + self._padding),
                               text="Fullscreen:")
        fullscreen_graphics_config = ToggleableTextButtonConfig(position=(fullscreen_text.rect.right + self._padding,
                                                                          fullscreen_text.rect.centery),
                                                                size=(200, 30),
                                                                colors=(Colors.PRIMARY, Colors.SECONDARY, Colors.ACCENT),
                                                                text="ugh", align="midleft")
        fullscreen_graphics = ToggleableTextButton(fullscreen_graphics_config)
        self.option_widgets = ({"fullscreen": fullscreen_text, "fullscreen button": fullscreen_graphics}), ({}), ({})

    def update_widget(self, num):
        for widget in self.option_widgets[num].values():
            widget.update()

    def render_widget(self, num):
        for widget in self.option_widgets[num].values():
            widget.blit()

    def update(self):
        super().update()
        self.options.update()
        for index, option in enumerate((self.graphics, self.keybinds, self.audio)):
            if option.toggled:
                self.current_option = index
        match self.current_option:
            case 0:
                if screen.get_flags() & pygame.FULLSCREEN:
                    text = "True"
                else:
                    text = "False"
                self.option_widgets[self.current_option]["fullscreen button"].text.text = text
        widgethandler.update()
        self.update_widget(self.current_option) if self.current_option is not None else None

    def render(self):
        screen.blit(self.background, (0, 0))
        screen.blit(self.bg_surf, self.bg_rect)
        screen.blit(self.title,
                    (screen_size[0] / 2 - self.title.get_width() / 2,
                     screen_size[1] * 0.1))
        widgethandler.blit()
        self.render_widget(self.current_option) if self.current_option is not None else None

    def startup(self):
        super().startup()

    def cleanup(self):
        super().cleanup()
