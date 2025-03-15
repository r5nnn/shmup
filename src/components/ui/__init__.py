"""Package containing widgets for use in the game's UI."""

from src.components.ui.text import Text, TextArray, TextArrayConfig
from src.components.ui.dropdown import TextDropdown
from src.components.ui import widgethandler
from src.components.ui.buttons.imagebutton import (
    ImageToggleButton,
    ImageClickButton,
    ImageRectClickButton,
    ImageRectToggleButton,
    ImageButtonConfig,
)
from src.components.ui.buttons.textbutton import (
    TextClickButton,
    TextToggleButton,
    TextRectClickButton,
    TextRectToggleButton,
    TextButtonConfig,
)
from src.components.ui.buttons.textbuttonarray import (
    TextToggleButtonArray,
    TextToggleButtonArrayConfig,
    TextClickButtonArray,
    TextClickButtonArrayConfig,
    TextRectToggleButtonArray,
    TextRectToggleButtonArrayConfig,
    TextRectClickButtonArray,
    TextRectClickButtonArrayConfig,
)
from src.components.ui.buttons.imagebuttonarray import (
    ImageToggleButtonArray,
    ImageToggleButtonArrayConfig,
    ImageClickButtonArray,
    ImageClickButtonArrayConfig,
)
from src.components.ui.buttons.togglegroup import (
    ToggleButtonGroup,
    ToggleArrayGroup,
)
