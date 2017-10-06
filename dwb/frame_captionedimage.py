import pygame
import images
from pathlib import Path
from frame import Frame
from frame_text import TextFrame


class CaptionedImage(Frame):
    """[SUMMARY]"""
    def __init__(self, screen: pygame.display, parent: Frame,
                 image_path: Path,
                 padx: int=0, pady: int=0,
                 text: str='CaptionedImage',
                 font_file: str or None=None, text_color: (int, int, int)=(0, 0, 0),
                 text_padx: int=0, text_pady: int=0,
                 bg_color: (int, int, int)=(255, 255, 255)) -> None:
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
        image_weight = 3
        text_weight = 1
        image_ratio = image_weight / (image_weight + text_weight)
        text_ratio = 1 - image_ratio
        max_image_size = (self.get_width(), self.get_height()*image_ratio)
        self._image = images.scale_image(images.load_image(image_path), max_image_size)
        self._image_rect = self._image.get_rect(midtop=(self.get_center()[0], self.get_y()))
        self._text_f = Frame(screen, parent=None, x=self.get_x(), y=self._image_rect.bottom, width=self.get_width(), height=round(self.get_height()*text_ratio))
        self._text_frame = TextFrame(screen, self._text_f, text, font_file, text_color, text_padx, text_pady)

    def draw(self):
        self._update_position()
        self._image_rect.midtop = (self.get_center()[0], self.get_y())
        self._text_f.set_position(y=self._image_rect.bottom)
        self._screen.blit(self._image, self._image_rect)
        self._text_frame.draw()


# Testing
if __name__ == '__main__':
    from pathlib import Path

    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('CaptionedImage Test')
    pygame.mouse.set_visible(0)

    running = True
    clock = pygame.time.Clock()

    f = Frame(screen, None, 0, 0, screen.get_width(), screen.get_height())
    ci = CaptionedImage(screen, f, str(Path('assets/img/compost/napkin.png')))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

        f.draw()
        ci.draw()

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()
