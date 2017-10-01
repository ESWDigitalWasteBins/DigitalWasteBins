import pygame
from frame import Frame
from frame_captionedimage import CaptionedImage


class Content(Frame):
    """Creates a single CaptionedImage."""
    def __init__(self, screen: pygame.display, parent: Frame,
                 image_path: str, text: str,
                 content_padx: int=0, content_pady: int=0,
                 bg_color: (int, int, int)=(0, 0, 0)) -> None:
        """
        [SUMMARY]

        Args:
            [PARAM1]: [DESCRIPTION]
            [PARAM2]: [DESCRIPTION]

        Attributes:
            [ATTR1]: [DESCRIPTION]
            [ATTR2]: [DESCRIPTION]
        """
        Frame.__init__(self, screen, parent)
        self._captioned_image = CaptionedImage(screen, self, image_path, text, padx=content_padx, pady=content_pady)
        self._bg_color = bg_color

    def draw(self) -> None:
        self._update_position()
        self._captioned_image.draw()
