import pygame
from frame import Frame


class TextFrame(Frame):
    """Frame for holding text."""

    def __init__(self, screen: pygame.display, parent: Frame,
                 font_file: str or None,
                 text: str, text_color: (int, int, int)=(0, 0, 0),
                 padx: int=0, pady: int=0) -> None:
        Frame.__init__(self, screen, parent=parent, padx=padx, pady=pady)
        print(self.get_width())
        font_size = self.get_height()
        font = pygame.font.Font(font_file, font_size)
        while True:
            self._text = font.render(text, True, text_color)
            if self._text.get_width() > self.get_width():
                font_size -= 10
                font = pygame.font.Font(None, font_size)
            else:
                break
        self._text_rect = self._text.get_rect(center=self.get_center())

    def draw(self) -> None:
        self._update_position()
        self._screen.blit(self._text, self._text_rect)


# Testing
if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('Frame Test')
    pygame.mouse.set_visible(0)

    running = True
    clock = pygame.time.Clock()

    f = Frame(screen, None, 0, 0, screen.get_width(), screen.get_height())
    print(f._bg_color)
    tf = TextFrame(screen, f, 'Text Frame', padx=500, pady=500)

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
        tf.draw()

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()