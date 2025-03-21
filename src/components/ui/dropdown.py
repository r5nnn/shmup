from __future__ import annotations

import logging
from typing import Callable, TYPE_CHECKING

from src.components.ui.buttons import (
    TextRectToggleButton,
    TextRectClickButtonArrayConfig,
    TextButtonConfig,
    TextRectClickButtonArray,
)
from src.components.ui.widgetutils import WidgetBase

if TYPE_CHECKING:
    import pygame
    from src.core.types import Colors, RectAlignments
    from collections.abc import Sequence


logger = logging.getLogger("src.components.ui")


class TextDropdown(WidgetBase):
    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        colors: Colors = None,
        audio_tags: list[str | None] | None = None,
        text_colors: Colors = None,
        font: pygame.font.Font | None = None,
        font_size: int = 32,
        choice_font_size: int = 24,
        *,
        choices: Sequence[str],
        start_choice: int | None = None,
        actions: tuple[Callable | None, ...] | Callable[[int], ...] | None = None,
        pass_index: bool = False,
        radius: int = 0,
        antialias: bool = False,
        align: RectAlignments = "topleft",
        sub_widget: bool = False,
    ):
        super().__init__(position, align, sub_widget=sub_widget)
        self.start_choice = start_choice
        self.chosen = (
            choices[0] if start_choice is None else choices[start_choice]
        )
        self.dropped = False
        head_config = TextButtonConfig(
            position=position,
            align=align,
            audio_tags=audio_tags,
            text_colors=text_colors,
            font=font,
            font_size=font_size,
            antialias=antialias,
            sub_widget=True,
        )
        self.head_button = TextRectToggleButton(
            head_config,
            size,
            self.chosen,
            on_toggle_off=lambda: setattr(self, "dropped", False),
            on_toggle_on=lambda: setattr(self, "dropped", True),
            radius=radius,
            colors=colors,
        )
        self.actions = actions
        self.pass_index = pass_index
        self.choices = choices
        actions_ = (
            tuple(
                lambda choice=choice: self.select_choice(choice)
                for choice in choices
            ),
            (),
        )
        options_config = TextRectClickButtonArrayConfig(
            audio_tags=audio_tags,
            align="topleft",
            text_colors=text_colors,
            font=font,
            font_size=choice_font_size,
            antialias=antialias,
            texts=(tuple(choices), ()),
            on_click=actions_,
            sizes=size,
            radius=radius,
            colors=colors,
        )
        self.option_button_arr = TextRectClickButtonArray(
            self.head_button.rect.bottomleft,
            (len(choices), 1),
            0,
            options_config,
            arr_sub_widget=True,
        )
        self.sub_widgets.extend((self.option_button_arr, self.head_button))
        logger.info("Created text dropdown widget %s.", repr(self))

    def blit(self) -> None: ...

    def update(self) -> None:
        self.option_button_arr.hidden = not self.dropped
        self.option_button_arr.disabled = not self.dropped

    def select_choice(self, choice: str) -> None:
        self.chosen = choice
        self.head_button.texts = (choice, choice)
        self.head_button.toggle_off_call(silent=True)
        if isinstance(self.actions, Callable):
            self.actions(self.choices.index(choice))
        elif (
            self.actions is not None
            and self.actions[self.choices.index(choice)] is not None and not self.pass_index
        ):
            self.actions[self.choices.index(choice)]()
        self.dropped = False
        logging.info("Selected new choice %s, closing popup, calling action if"
                     " not None and setting text of dropdown head to new "
                     "choice.", choice)

    def contains(self, x: int, y: int) -> bool:
        super().contains(x, y)
        return self.head_button.contains(x, y)

    def __repr__(self):
        return (f"{self.__class__.__name__}(position={self.x, self.y!r}, "
                f"size={self.head_button.rect.size!r}, "
                f"colors={self.head_button.colors!r}, "
                f"audio_tags={self.head_button.audio_tags!r}, "
                f"text_colors={self.head_button.text_colors!r}, "
                f"font={self.head_button.text_object.font!r}, "
                f"font_size={self.head_button.text_object.font_size!r}, "
                f"choices={self.choices!r}, "
                f"start_choice={self.start_choice!r}, "
                f"actions={self.actions!r}, "
                f"radius={self.head_button.radius!r}, "
                f"antialias={self.head_button.text_object.antialias!r}, "
                f"align={self.align!r}, sub_widget={self.sub_widget!r}")
