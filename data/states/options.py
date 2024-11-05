from data.components.ui import Popup, PopupConfig, TextButton, TextButtonConfig
from data.core import Colors
from data.core.prepare import screen_center
from data.states.state import State


class Options(State):
    def __init__(self):
        super().__init__()
        text_btn_config = TextButtonConfig(position=screen_center, size=(100, 30),
                                           text='click', align='midleft',
                                           colors={
                                               'default': Colors.BACKGROUND,
                                               'hovered': Colors.FOREGROUND,
                                               'clicked': Colors.ACCENT
                                           })
        x= TextButton(text_btn_config)
        text_btn_config.text = 'bye'
        x1=TextButton(text_btn_config)
        text_btn_config.text = '~'
        x2=TextButton(text_btn_config)
        popup_config = PopupConfig(position=screen_center, size=(400, 100), buttons=(x,x1, x2), text='HELLO BRO',
                                   padding=20, color=(14, 14, 14))
        self.popup = Popup(popup_config)
        self.widgets = (self.popup,)

    def update_screen(self):
        ...

    def update(self):
        super().update()

    def render(self):
        super().render()

    def startup(self):
        super().startup()

    def cleanup(self):
        super().cleanup()