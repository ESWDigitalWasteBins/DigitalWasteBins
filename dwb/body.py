import pygame
from frame import Frame
from content import Content


class Body(Frame):
    """Holds a bunch of Content()."""

    def __init__(self, screen: pygame.display,
                 image_path: str, text: str,
                 x: int, y: int,
                 width: int, height: int) -> None:
        Frame.__init__(self, screen, None, x, y, width, height)
        self._content = Content(screen, self, image_path,
                                text, content_padx=20, content_pady=50)

    def draw(self):
        self._content.draw()
