from typing import Literal

RectAlignments = Literal[
    'topleft', 'midtop', 'topright',
    'midleft', 'center', 'midright',
    'bottomleft', 'midbottom', 'bottomright'
]

from data.components.ui.button import TextButtonConfig, TextButton, \
    ImageButtonConfig, ImageButton
from data.components.ui.text import Text, WrappedText