import pygame
from frame import BaseFrame, Frame


class TextFrame(Frame):
    def __init__(self, screen: pygame.display, master: BaseFrame or Frame,
                 text: str, padx: int=0, pady: int=0) -> None:
        Frame.__init__(self, screen, master, padx, pady)
        self._text = text

    def draw(self) -> None:
        self._update_position()
        font = pygame.font.Font(None, self.get_height())
        text = font.render(self._text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.get_center())
        self._screen.blit(text, text_rect)


class Title(BaseFrame):
    def __init__(self, screen: pygame.display,
                 x: int, y: int, width: int, height: int,
                 text: str, bg_color: (int, int, int)=(0, 0, 0)) -> None:
        BaseFrame.__init__(self, screen, x, y, width, height)
        self._bg_color = bg_color
        self._text_frame = TextFrame(screen, self, text)

    def draw(self) -> None:
        pygame.draw.rect(self._screen, self._bg_color, (self.get_x(), self.get_y(), self.get_width(), self.get_height()))
        self._text_frame.draw()


class Display():
    def __init__(self, title: Title):
        self._title = title

    def draw(self):
        self._title.draw()


if __name__ == '__main__':
    TEXT_WEIGHT = 1
    CONTENT_WEIGHT = 5
    TEXT_RATIO = TEXT_WEIGHT / (TEXT_WEIGHT + CONTENT_WEIGHT)
    CONTENT_RATIO = 1 - TEXT_RATIO

    BLUE = (0, 57, 166)

    pygame.init()
    # screen = pygame.display.set_mode((350, 700))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('Display Test')

    title = Title(screen, 0, 0,
                  screen.get_width(), int(TEXT_RATIO*screen.get_height()),
                  'RECYCLE', BLUE)
    display = Display(title)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

        display.draw()

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()
