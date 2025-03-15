from __future__ import annotations

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


class TextDropdown(WidgetBase):
    def __init__(
        self,
        position: tuple[int, int],
        size: tuple[int, int],
        colors: Colors = None,
        audio_tags: list[str | None] | None = None,
        text_colors: Colors = None,
        font: pygame.font.Font | None = None,
        font_size: int = 32, choice_font_size: int = 24,
        *,
        choices: tuple[str, ...],
        start_choice: int | None = None,
        actions: tuple[Callable | None, ...] | None = None,
        radius: int = 0,
        antialias: bool = False,
        align: RectAlignments = "topleft",
    ):
        super().__init__(position, align)
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

    def blit(self) -> None:
        self.head_button.blit()
        if self.dropped:
            self.option_button_arr.blit()

    def update(self) -> None:
        super().update()
        self.head_button.update()
        if self.dropped:
            self.option_button_arr.update()

    def select_choice(self, choice: str) -> None:
        self.chosen = choice
        self.head_button.texts = (choice, choice)
        self.head_button.toggle_off_call(silent=True)
        if (
            self.actions is not None
            and self.actions[self.choices.index(choice)] is not None
        ):
            self.actions[self.choices.index(choice)]()
        self.dropped = False

    def contains(self, x: int, y: int) -> bool:
        super().contains(x, y)
        return self.head_button.contains(x, y)
