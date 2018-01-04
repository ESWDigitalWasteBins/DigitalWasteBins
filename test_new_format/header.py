import pygame
from frame import Frame
from text import TextFrame


class Header(Frame):
    def __init__(self, screen: pygame.display,
                 x: int, y: int, width: int, height: int,
                 font_file: str or None,
                 text: str='Header', text_color: (int, int, int)=(0, 0, 0),
                 text_padx: int=0, text_pady: int=0,
                 bg_color: (int, int, int)=(255, 255, 255)) -> None:
        Frame.__init__(self, screen, None, x, y, width, height)
        self._bg_color = bg_color
        self._text_frame = TextFrame(
            screen, self, text, font_file, text_color, text_padx, text_pady)

    def draw(self) -> None:
        Frame.draw(self)
        self._text_frame.draw()
