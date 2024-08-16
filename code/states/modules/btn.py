from typing import Callable, TYPE_CHECKING, override

import pygame

from .img import Img
from .txt import Txt
from .constants import rect_allignments, button_colors, white

# avoids relative import error while making pycharm happy
# (shows error when type resides in another module when using
# PEP 563 – Postponed Evaluation of Annotations)
if TYPE_CHECKING:
    from ...game import Game


class _Btn:
    """
    Attributes:
        clicked: Boolean which shows if any button of the
        _Btn class or any of its children are pressed.
    """
    clicked: bool = False

    def __init__(self,
                 game: 'Game',
                 coords: tuple[int, int],
                 width: int,
                 height: int,
                 func: Callable = None,
                 col_btn: list[tuple[int, int, int]] = button_colors,
                 btn_allign: rect_allignments = 'center'):
        """
        Parent class for all types of buttons.
        Creates the background rect and adds click detection and sfx.

        Args:
            game: Script for running game.
            coords: X and Y coordinates of button background rect.
            width: Width of button background rect.
            height: Height of button background rect.
            func: Function to be called upon button being clicked,
            ignored if None.
            col_btn: RGB values of button background rect color when button is
            clicked, hovered, or neither.
            [0] is the color when neither,
            [1] is the color when hovered,
            and [2] is the color when clicked.
            btn_allign: The allignment that the button coordinates point to.
        """
        self.game = game
        self.func = func
        self.col_btn = col_btn
        self.clicked = False
        # button background rect
        self.rect = pygame.Rect(coords[0], coords[1], width, height)
        self.current_btn_col = self.col_btn[0]
        setattr(self.rect, btn_allign, (coords[0], coords[1]))

    def on_click(self, event: pygame.MOUSEBUTTONDOWN) -> None:
        """
        Call when mouse is clicked.
        Collision checks the mouse with the button, plays sfx.
        Also handles cancelling click through a right click.

        Args:
            event: Mouse button that was clicked.
        """
        if self.rect.collidepoint(self.game.pos) and \
                not _Btn.clicked and event.button == 1:
            self.clicked = True
            _Btn.clicked = True
            self.current_btn_col = self.col_btn[2]
            self.game.btn_sfx.set_volume(0.2)
            self.game.btn_sfx.play_audio("click", override=True)
        if event.button == 3:  # right click to cancel click
            self.clicked = False
            _Btn.clicked = False

    def on_release(self, event: pygame.MOUSEBUTTONUP) -> None:
        """
        Call when mouse released.
        Checks if mouse was clicked on MOUSEDOWN, plays sfx.
        Calls function assigned when clicking button.

        Args:
            event: Mouse button that was released.
        """
        if self.clicked and event.button == 1:
            self.clicked = False
            _Btn.clicked = False
            self.game.btn_sfx.set_volume(0.15)
            self.game.btn_sfx.play_audio("click", override=True)
            self.func() if callable(self.func) else None


# noinspection PyMethodOverriding
class BtnTxt(_Btn, Txt):
    def __init__(self,
                 game: 'Game',
                 coords: tuple[int, int],
                 width: int,
                 height: int,
                 text: str,
                 func: Callable = None,
                 font: pygame.font.Font = None,
                 font_size: int = None,
                 col_btn: list[tuple[int, int, int]] = button_colors,
                 col_txt: list[tuple[int, int, int]] = None,
                 btn_allign: rect_allignments = 'center',
                 txt_allign: rect_allignments = 'center',
                 wrap_width: int = None):
        """
        Class for buttons that only need text displayed on the label.
        Creates text for button through parent class Txt.

        Args:
            text: String of text to be displayed on button label.
            col_txt: RGB valies of button text color when button is clicked,
            hovered or neither.
            [0] is the color when neither,
            [1] is the color when hovered,
            and [2] is the color when clicked.
            btn_allign:
            txt_allign:
            wrap_width: Width in ptx of when text should start wrapping.
        """
        _Btn.__init__(self, game, coords, width,
                      height, func, col_btn, btn_allign)
        self.col_txt = col_txt if col_txt is not None else [white, white, white]
        # wrap_width must be defined before calling parent class Txt
        self.wrap_width = self.rect.width if wrap_width is None else wrap_width
        self.current_txt_col = self.col_txt[0]
        Txt.__init__(self, (self.rect.centerx, self.rect.centery),
                     text, font if font is not None else None,
                     size=font_size if font_size is not None else None,
                     allign=txt_allign,
                     wrap_width=self.wrap_width)

    @override
    def update(self, surface: pygame.Surface) -> None:
        """
        Renders text, blits button rect to surface, handles user inputs.

        Args:
            surface: Surface which button will be blitted to.
        """
        # main button rect
        pygame.draw.rect(surface, self.current_btn_col, self.rect)
        # text to be rendered on top of button
        Txt.update(self, surface, self.current_txt_col)
        if self.rect.collidepoint(self.game.pos) and not _Btn.clicked:
            # button is hovered not clicked
            self.current_btn_col = self.col_btn[1]
            self.current_txt_col = self.col_txt[1]
        elif not _Btn.clicked:
            # button is not hovered or clicked
            self.current_btn_col = self.col_btn[0]
            self.current_txt_col = self.col_txt[0]
        if self.clicked:
            # button is clicked
            self.current_btn_col = self.col_btn[2]
            self.current_txt_col = self.col_txt[2]


class BtnBack(BtnTxt):
    def __init__(self,
                 game: 'Game',
                 coords: tuple[int, int],
                 width: int,
                 height: int,
                 text: str = 'Back',
                 font_size: int = None,
                 btn_allign: rect_allignments = 'center'):
        """
        Class for making buttons that go back a screen via the state stack.
        Func auto assigned.
        For additional info on args, view help on parent class BtnTxt.
        """
        super().__init__(game, coords, width, height,
                         text, font_size=font_size,
                         btn_allign=btn_allign)
        self.func = self.back

    def back(self) -> None:
        """Pops top item out of the state stack."""
        self.game.state_stack[-1].back(play_sfx=False)


class BtnImg(_Btn, Img):
    def __init__(self,
                 game: 'Game',
                 coords: tuple[int, int],
                 width: int,
                 height: int,
                 img: pygame.Surface,
                 img_coords: tuple[int, int] = None,
                 scale: int = 1,
                 func: Callable = None,
                 col_btn: list[tuple[int, int, int]] = button_colors,
                 btn_allign: rect_allignments = 'center',
                 img_allign: rect_allignments = 'center'):
        """
        Class for making buttons with images displayed on the labels.
        Uses parent class Img to place image onto label of button.

        Args:
            img_allign: References which point on the button
            rect the coordinates of the image point to.

        For additional info on args, view help on parent classes Img and _Btn.
        """
        _Btn.__init__(self, game, coords, width, height,
                      func, col_btn, btn_allign)
        Img.__init__(self,
                     img_coords if img_allign != 'center' else self.rect.center,
                     img, scale, img_allign)

    @override
    def update(self, surface: pygame.Surface) -> None:
        """
        Renders button rect, blits image and handles user input.

        Args:
            surface: Surface which button will be blitted to.
        """
        # main button rect
        pygame.draw.rect(surface, self.current_btn_col, self.rect)
        Img.update(self, surface)  # image surface
        if self.rect.collidepoint(self.game.pos) and not _Btn.clicked:
            # button is hovered not clicked
            self.current_btn_col = self.col_btn[1]
        elif not _Btn.clicked:
            # button is not hovered or clicked
            self.current_btn_col = self.col_btn[0]
        if self.clicked:
            # button is clicked
            self.current_btn_col = self.col_btn[2]
