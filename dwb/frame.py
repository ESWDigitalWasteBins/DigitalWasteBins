import pygame


class BaseFrame:
    def __init__(self, screen: pygame.display,
                 x: int=0, y: int=0,
                 width: int=100, height: int=100):
        self._screen = screen
        self._position = self._x, self._y = (x, y)
        self._size = self._width, self._height = (width, height)

    def set_position(self, x: int=0, y: int=0) -> None:
        self._position = self._x, self._y = (x, y)

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def get_position(self) -> (int, int):
        return self._position

    def get_width(self) -> int:
        return self._width

    def get_height(self) -> int:
        return self._height

    def get_size(self) -> (int, int):
        return self._size


class Frame(BaseFrame):
    def __init__(self, screen: pygame.display, master: BaseFrame or 'Frame',
                 padx: int=0, pady: int=0,
                 bg_color: (int, int, int)=(0, 0, 0)):
        x, y = master.get_x() + padx, master.get_y() + pady
        width, height = master.get_width() - 2*padx, master.get_height() - 2*pady
        BaseFrame.__init__(self, screen, x, y, width, height)
        self._screen = screen
        self._master = master
        self._padx = padx
        self._pady = pady
        self._bg_color = bg_color

    def draw(self) -> None:
        self.update_position(self._master.get_x(), self._master.get_y())
        pygame.draw.rect(self._screen, self._bg_color, (self._x, self._y, self._width, self._height))

    def update_position(self, x: int=0, y: int=0) -> None:
        self._position = self._x, self._y = (self._master.get_x() + self._padx, self._master.get_y() + self._pady)


# Test Frame
if __name__ == '__main__':
    pygame.init()

    # screen = pygame.display.set_mode((500, 500))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    s = pygame.Surface((1920, 1080))
    pygame.display.set_caption('Frame Test')
    pygame.mouse.set_visible(0)

    running = True
    clock = pygame.time.Clock()

    topbase = BaseFrame(screen, width=screen.get_width(), height=screen.get_height()//2)
    botbase = BaseFrame(screen, y=topbase.get_height(), width=screen.get_width(), height=screen.get_height()//2)
    topframe = Frame(screen, topbase, padx=100, pady=100, bg_color=(255, 0, 0))
    botframe = Frame(screen, botbase, padx=100, pady=100, bg_color=(0, 255, 0))
    subframe = Frame(screen, topframe, bg_color=(0, 255, 255), padx=50, pady=100)
    y = -screen.get_height()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

        y += 5
        screen.fill(0)
        topbase.set_position(0, y)
        botbase.set_position(0, y + topbase.get_height())
        topframe.draw()
        botframe.draw()
        subframe.draw()

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()
