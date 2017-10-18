import pygame
from frame import Frame
from frame_text import TextFrame


class Header(Frame):
    def __init__(self, screen: pygame.display,
                 x: int, y: int, width: int, height: int,
                 font_file: str or None,
                 text: str='Header', text_color: (int, int, int)=(0, 0, 0),
                 text_padx: int=0, text_pady: int=0,
                 bg_color: (int, int, int)=(255, 255, 255)) -> None:
        Frame.__init__(self, screen, None, x, y, width, height)
        self._bg_color = bg_color
        self._text_frame = TextFrame(screen, self, text, font_file, text_color, text_padx, text_pady)

    def draw(self) -> None:
        Frame.draw(self)
        self._text_frame.draw()


if __name__ == '__main__':
    from pathlib import Path

    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('Header Test')
    pygame.mouse.set_visible(0)

    running = True
    clock = pygame.time.Clock()

    header = Header(screen, 0, 0, screen.get_width(), screen.get_height(), font_file=str(Path('./assets/fnt/arial.ttf')))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

        header.draw()

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()
