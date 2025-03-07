"""Package containing components that help run the game."""
from src.components.audio import Audio, background_audio, button_audio
from src.components.colors import shift_rgb, ColorGradient
from src.components.ui.text import Text, TextArray
from src.components.ui.buttons.imagebutton import (
    ImageToggleButton, ImageClickButton, ImageRectClickButton,
    ImageRectToggleButton, ImageButtonConfig)
from src.components.ui.buttons.textbutton import (
    TextClickButton, TextToggleButton, TextRectClickButton,
    TextRectToggleButton, TextButtonConfig)
from src.components.ui.buttons.textbuttonarray import (
    TextToggleButtonArray, TextToggleButtonArrayConfig, TextClickButtonArray,
    TextClickButtonArrayConfig, TextRectToggleButtonArray,
    TextRectToggleButtonArrayConfig, TextRectClickButtonArray,
    TextRectClickButtonArrayConfig)
from src.components.ui.buttons.imagebuttonarray import (
    ImageToggleButtonArray, ImageToggleButtonArrayConfig,
    ImageClickButtonArray,
    ImageClickButtonArrayConfig)
from src.components.ui.buttons.togglegroup import (
    ToggleButtonGroup, ToggleArrayGroup)
