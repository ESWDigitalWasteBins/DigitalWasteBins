import pygame
from pathlib import Path


def load_image(image_path: Path, colorkey=None):
    """
    Load an image from the image_path with optional colorkey.
    Uses convert_alpha() to increase alpha performance.

    Args:
        image_path: path to image file
        colorkey: a three-tuple or -1 representing the color that you
                  want transparent instead of the image's actual color
    """
    try:
        image = pygame.image.load(str(image_path)).convert_alpha()
    except pygame.error:
        print('Cannot load image:', image_path)
        raise SystemExit(str(pygame.compat.geterror()))
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image  # , image.get_rect()


def scale_image(image: pygame.image, size: (int, int), limit: bool=False) -> pygame.image:
    """
    Return a scaled image to the smaller scaled size.

    Args:
        image: a pygame surface (image)
        size: a two tuple representing the desired width and height
        limit(=False): turn on to limit scaling to maximum size of image
    """
    width, height = size
    iwidth, iheight = image.get_size()  # image dimensions
    scale_x = width / iwidth            # scale by width
    scale_y = height / iheight          # scale by height
    scale = min(scale_x, scale_y)       # scale by the smaller value
    if limit and scale > 1:
        scale = 1
    return pygame.transform.scale(image, (int(scale*iwidth), int(scale*iheight)))


if __name__ == '__main__':
    from frame import Frame

    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('Image Test')

    clock = pygame.time.Clock()
    running = True

    image_path = 'images\\items\\1.png'
    image = load_image(image_path)
    scaled = scale_image(image, (screen.get_width(), screen.get_height()))

    class CaptionedImage(Frame):
        """[SUMMARY]"""
        def __init__(self, screen: pygame.display, parent: Frame,
                     image_path: str, text: str,
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
            iscale = 0.8
            tscale = 1 - iscale
            isize = (iscale*self.get_width(), iscale*self.get_height())
            self._image = scale_image(load_image(image_path), isize)
            self._image_rect = self._image.get_rect(midtop=(self.get_center()[0], self.get_y()))
            self._text = pygame.font.Font(None, 100).render(text, True, (255, 255, 255))
            self._text_rect = self._text.get_rect(midbottom=(self.get_center()[0], self.get_y()+self.get_height()))

        def draw(self):
            self._update_position()
            self._image_rect.midtop = (self.get_center()[0], self.get_y())
            self._text_rect.midbottom = (self.get_center()[0], self.get_y()+self.get_height())
            self._screen.blit(self._image, self._image_rect)
            self._screen.blit(self._text, self._text_rect)


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
            # pygame.draw.rect(self._screen, self._bg_color, (self.get_x(), self.get_y(), self.get_width(), self.get_height()))
            self._captioned_image.draw()


    class Body(Frame):
        """Holds a bunch of Content()."""
        def __init__(self, screen: pygame.display,
                     image_path: str, text: str,
                     x: int, y: int,
                     width: int, height: int) -> None:
            Frame.__init__(self, screen, None, x, y, width, height)
            self._content = Content(screen, self, image_path, text)

        def draw(self):
            self._content.draw()

    body = Body(screen, 'images\\items\\4.png', 'testing 123', 0, 0, screen.get_width(), screen.get_height())

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

        body.draw()

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()
