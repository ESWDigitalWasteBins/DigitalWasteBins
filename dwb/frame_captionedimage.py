import pygame
import images
from pathlib import Path
from frame import Frame


class CaptionedImage(Frame):
    """[SUMMARY]"""
    def __init__(self, screen: pygame.display, parent: Frame,
                 image_path: Path, text: str,
                 padx: int=0, pady: int=0,
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
        Frame.__init__(self, screen, parent, padx=padx, pady=pady, bg_color=bg_color)
        iscale = 0.7
        tscale = 1 - iscale
        isize = (iscale*self.get_width(), iscale*self.get_height())
        self._image = images.scale_image(images.load_image(image_path), isize)
        self._image_rect = self._image.get_rect(midtop=(self.get_center()[0], self.get_y()))
        self._text = pygame.font.Font(None, 100).render(text, True, (255, 255, 255))
        self._text_rect = self._text.get_rect(midbottom=(self.get_center()[0], self.get_y()+self.get_height()))

    def draw(self):
        self._update_position()
        self._image_rect.midtop = (self.get_center()[0], self.get_y())
        self._text_rect.midbottom = (self.get_center()[0], self.get_y()+self.get_height())
        self._screen.blit(self._image, self._image_rect)
        self._screen.blit(self._text, self._text_rect)
