from __future__ import annotations

import logging
from typing import Callable, TYPE_CHECKING, override

from src.components.ui.buttons import (
    TextRectToggleButton,
    TextRectClickButtonArrayConfig,
    TextButtonConfig,
    TextRectClickButtonArray,
)
from src.components.ui.widgetutils import CompositeWidgetBase, WidgetBase

if TYPE_CHECKING:
    import pygame
    from src.core.types import Colors, RectAlignments
    from collections.abc import Sequence


logger = logging.getLogger("src.components.ui")


class TextDropdown(CompositeWidgetBase):
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
        actions: (
            tuple[Callable | None, ...] | Callable[[int], ...] | None
        ) = None,
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
            sub_widget=True,
        )
        logger.info("Created text dropdown widget %s.", self)

    @override
    def blit(self) -> None:
        self.head_button.blit()
        if self.dropped:
            self.option_button_arr.blit()

    @override
    def update(self, disabled_sub_widgets: list[WidgetBase] = ()) -> None:
        if not super().update(disabled_sub_widgets=disabled_sub_widgets):
            return
        if self.head_button not in disabled_sub_widgets:
            self.head_button.update(disabled_sub_widgets)
        if self.dropped and self.option_button_arr not in disabled_sub_widgets:
            self.option_button_arr.update(disabled_sub_widgets)

    def select_choice(self, choice: str) -> None:
        self.chosen = choice
        self.head_button.texts = (choice, choice)
        self.head_button.toggle_off_call(silent=True)
        if isinstance(self.actions, Callable):
            self.actions(self.choices.index(choice))
        elif (
            self.actions is not None
            and self.actions[self.choices.index(choice)] is not None
            and not self.pass_index
        ):
            self.actions[self.choices.index(choice)]()
        self.dropped = False
        logging.info(
            "Selected new choice %s, closing popup, calling action if"
            " not None and setting text of dropdown head to new "
            "choice.",
            choice,
        )

    @override
    def contains(self, x: int, y: int) -> list[WidgetBase]:
        if not super().contains(x, y):
            return []
        head_contains = self.head_button.contains(x, y)
        if not self.dropped:
            return head_contains
        dropped_contains = self.option_button_arr.contains(x, y)
        return head_contains + dropped_contains

    @override
    def __str__(self):
        return f"{super().__str__()[:-1]} choices={self.choices}>"
