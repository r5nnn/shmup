"""Places and blits buttons onto surfaces and handles user input."""
from typing import Callable, Literal, TYPE_CHECKING, override

import pygame

from .img import Img
from .txt import Txt

if TYPE_CHECKING:
    from ...game import Game


class Btn:
    clicked = False

    def __init__(self, game: 'Game',
                 x: int, y: int, width: int, height: int, func: Callable = None, sfx: str = None,
                 col_btn: list[tuple[int, int, int]] = [(30, 30, 30), (35, 35, 35), (85, 85, 85)],
                 btn_ref: Literal['topleft', 'midtop', 'topright',
                                  'midleft', 'center', 'midright',
                                  'bottomleft', 'midbottom', 'bottomright'] = 'center'):
        """Initialises Btn with Txt parent class.

        Creates button background rect, Sfx object, and text through parent class Txt.

        Args:
            game: Script for running game.
            x: X coordinate of button background rect.
            y: Y coordinate of button background rect.
            width: Width of button background rect.
            height: Height of button background rect.
            func: Function to be called upon button being clicked, ignored if None.
            sfx: Path to .wav audio file played when button clicked.
            col_btn: RGB values of button background rect color when button is clicked, hovered, or neither. [0] is the color when neither, [1] is the color
            when hovered, and [2] is the color when clicked.
            col_txt: RGB valies of button text color when button is clicked, hovered or neither. [0] is the color when neither, [1] is the color when hovered,
            and [2] is the color when clicked.
            btn_ref: References which point on the button rect the coordinates point to.

        For additional info on args, view help on parent class Txt.
        """
        self.game = game
        self.func = func
        self.col_btn = col_btn
        self.clicked = False
        self.rect = pygame.Rect(x, y, width, height)  # create button background rect
        self.sfx = pygame.mixer.Sound(self.game.click_btn_sfx if sfx is None else sfx)
        self.current_btn_col = self.col_btn[0]
        setattr(self.rect, btn_ref, (x, y))

    def on_click(self, event) -> None:
        if self.rect.collidepoint(self.game.pos) and not Btn.clicked and event.button == 1:
            self.clicked = True
            Btn.clicked = True
            self.current_btn_col = self.col_btn[2]
            self.sfx.set_volume(0.2)
            self.game.channel_btn.play(self.sfx)
        if event.button == 3:  # right click to cancel click
            self.clicked = False
            Btn.clicked = False

    def on_release(self, event) -> None:
        if self.clicked and event.button == 1:
            self.clicked = False
            Btn.clicked = False
            self.sfx.set_volume(0.15)
            self.game.channel_btn.play(self.sfx)
            self.func() if callable(self.func) else None


# noinspection PyMethodOverriding
class BtnTxt(Btn, Txt):
    """
    Attributes:
        clicked: A boolean indicating if any button has been clicked or not
    """

    def __init__(self, game: 'Game',
                 size: int, x: int, y: int, width: int, height: int, text: str, func: Callable = None, font_path: str = None, sfx: str = None,
                 col_btn: list[tuple[int, int, int]] = [(30, 30, 30), (35, 35, 35), (85, 85, 85)],
                 col_txt: list[tuple[int, int, int]] = [(255, 255, 255), (255, 255, 255), (255, 255, 255)],
                 btn_ref: Literal['topleft', 'midtop', 'topright',
                                  'midleft', 'center', 'midright',
                                  'bottomleft', 'midbottom', 'bottomright'] = 'center',
                 wrap: bool = False, wrapwidth: int = None):
        """Initialises Btn with Txt parent class.

        Creates button background rect, Sfx object, and text through parent class Txt.

        Args:
            game: Script for running game.
            x: X coordinate of button background rect.
            y: Y coordinate of button background rect.
            width: Width of button background rect.
            height: Height of button background rect.
            func: Function to be called upon button being clicked, ignored if None.
            sfx: Path to .wav audio file played when button clicked.
            col_btn: RGB values of button background rect color when button is clicked, hovered, or neither. [0] is the color when neither, [1] is the color
            when hovered, and [2] is the color when clicked.
            col_txt: RGB valies of button text color when button is clicked, hovered or neither. [0] is the color when neither, [1] is the color when hovered,
            and [2] is the color when clicked.
            btn_ref: References which point on the button rect the coordinates point to.

        For additional info on args, view help on parent class Txt.
        """
        Btn.__init__(self, game, x, y, width, height, func, sfx, col_btn, btn_ref)
        self.col_txt = col_txt
        # wrapwidth must be changed before calling parent class init
        self.wrapwidth = self.rect.width if wrapwidth is None else wrapwidth
        self.current_txt_col = self.col_txt[0]
        # create text for button using parent Txt class
        Txt.__init__(self, self.game.font_dir if font_path is None else font_path, size,
                     x=self.rect.centerx, y=self.rect.centery, text=text, ref='center', wrap=wrap, wrapwidth=self.wrapwidth)

    @override
    def update(self, surface: pygame.Surface) -> None:
        """Renders text blits button rect to surface, handles user inputs.

        Args:
            surface: Surface which button will be blitted to.
        """
        pygame.draw.rect(surface, self.current_btn_col, self.rect)  # rect must be drawn before text is blitted to stop overlap
        Txt.update(self, surface, self.current_txt_col)  # renders text using parent class
        if self.rect.collidepoint(self.game.pos) and not Btn.clicked:
            # button is hovered not clicked
            self.current_btn_col = self.col_btn[1]
            self.current_txt_col = self.col_txt[1]
        elif not Btn.clicked:
            # button is not hovered or clicked
            self.current_btn_col = self.col_btn[0]
            self.current_txt_col = self.col_txt[0]
        if self.clicked:
            self.current_btn_col = self.col_btn[2]
            self.current_txt_col = self.col_txt[2]


class BtnBack(BtnTxt):

    def __init__(self, game: 'Game', size: int, x: int, y: int, width: int, height: int, text='Back', btn_ref='center'):
        super().__init__(game, size, x, y, width, height, text, col_btn=[(30, 30, 30), (35, 35, 35), (85, 85, 85)],
                         col_txt=[(255, 255, 255), (255, 255, 255), (255, 255, 255)], btn_ref=btn_ref)
        self.func = self.back

    def back(self):
        """Pops top item out of the state stack."""
        self.game.state_stack[-1].on_exit()
        self.game.state_stack[-1].exit_state()


class BtnImg(Btn, Img):
    def __init__(self, game: 'Game',
                 x: int, y: int, width: int, height: int, img: pygame.Surface, imgx: int = None, imgy: int = None, scale: int = 1, func: Callable = None,
                 sfx: str = None,
                 col_btn: list[tuple[int, int, int]] = [(30, 30, 30), (35, 35, 35), (85, 85, 85)],
                 btn_ref: Literal['topleft', 'midtop', 'topright',
                                  'midleft', 'center', 'midright',
                                  'bottomleft', 'midbottom', 'bottomright'] = 'center',
                 img_ref: Literal['topleft', 'midtop', 'topright',
                                  'midleft', 'center', 'midright',
                                  'bottomleft', 'midbottom', 'bottomright'] = 'center'):
        """Initialises Btn with Img parent class.

        Creates button background rect, Sfx object, and img through parent class Img.

        Args:
            game: Script for running game.
            x: X coordinate of button background rect.
            y: Y coordinate of button background rect.
            width: Width of button background rect.
            height: Height of button background rect.
            imgx: X coordinate of image with refrence to button based on img_ref
            func: Function to be called upon button being clicked, ignored if None.
            sfx: Path to .wav audio file played when button clicked.
            col_btn: RGB values of button background rect color when button is clicked, hovered, or neither. [0] is the color when neither, [1] is the color
            when hovered, and [2] is the color when clicked.
            btn_ref: References which point on the button rect the coordinates point to.

        For additional info on args, view help on parent class Img.
        """
        Btn.__init__(self, game, x, y, width, height, func, sfx, col_btn, btn_ref)
        # create img for button using parent Img class
        Img.__init__(self, imgx if imgx is not None else self.rect.centerx, imgy if imgy is not None else self.rect.centery, img, scale, img_ref)

    def update(self, surface: pygame.Surface) -> None:
        """Renders text blits button rect to surface, handles user inputs.

        Args:
            surface: Surface which button will be blitted to.
        """
        pygame.draw.rect(surface, self.current_btn_col, self.rect)  # rect must be drawn before text is blitted to stop overlap
        Img.update(self, surface)  # renders text using parent class
        if self.rect.collidepoint(self.game.pos) and not Btn.clicked:
            # button is hovered not clicked
            self.current_btn_col = self.col_btn[1]
        elif not Btn.clicked:
            # button is not hovered or clicked
            self.current_btn_col = self.col_btn[0]
        if self.clicked:
            self.current_btn_col = self.col_btn[2]