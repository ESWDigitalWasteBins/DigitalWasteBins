import pygame


class Frame(pygame.Surface):
    """BaseFrame class for layout with position and size."""
    def __init__(self, screen: pygame.display, master: 'Frame'=None,
                 x: int=None, y: int=None,
                 width: int=None, height: int=None,
                 padx: int=0, pady: int=0,
                 bg_color: (int, int, int)=(0, 0, 0)):
        """
        Initialize Frame as subclass of pygame.Surface. Must have a
        master or position and size based on screen.

        Args:
            screen: screen to draw on
            x: x-coordinate of top-left corner
            y: y-coordinate of top-left corner
            width: width of frame
            height: height of frame
            padx(=0): horizontal padding
            pady(=0): vertical padding
            bg_color(=(0, 0, 0)): background color of Frame, a 3-tuple of ints
        """
        if master is None:
            assert all(type(x) is int for x in (x, y, width, height, padx, pady))
            self._master = self
        else:
            assert isinstance(master, Frame), 'master is not Frame()'
            x, y = master.get_x() + padx, master.get_y() + pady
            width = master.get_width() - 2*padx
            height = master.get_height() - 2*pady
            self._master = master
        pygame.Surface.__init__(self, (width, height))
        self._screen = screen
        self._position = self._x, self._y = (x, y)
        self._padx = padx
        self._pady = pady
        self._bg_color = bg_color

    def __str__(self) -> str:
        return 'Frame(master={}, x={}, y={}, width={}, height={}, padx={}, pady={})'.format('self' if self._master is self else self._master, self.get_x(), self.get_y(), self.get_width(), self.get_height(), self._padx, self._pady)

    def draw(self) -> None:
        """Draw a rectangle representing this Frame's covering."""
        self._update_position()
        pygame.draw.rect(self._screen, self._bg_color, (self._x, self._y, self.get_width(), self.get_height()))

    def _update_position(self) -> None:
        """Update position of Frame based on master, used when drawing."""
        self._position = self._x, self._y = (self._master.get_x() + self._padx,
                                             self._master.get_y() + self._pady)

    def set_position(self, x: int=None, y: int=None) -> None:
        """
        Set frame's top-left coordinate, unchanged if not specified.

        Args:
            x(=0): update frame's top-left x coordinate
            y(=0): update frame's top-left x coordinate
        """
        if x is not None:
            self._x = x
        if y is not None:
            self._y = y
        self._position = (self._x, self._y)

    def get_x(self) -> int:
        """Return top-left x coordinate."""
        return self._x

    def get_y(self) -> int:
        """Return top-left y coordinate."""
        return self._y

    def get_position(self) -> (int, int):
        """
        Return 2-tuple of ints representing top-left (x, y)
        coordinate.
        """
        return self._position

    def get_center(self) -> (int, int):
        """
        Return 2-tuple of ints representing center (x, y)
        coordinate.
        """
        return (self.get_x() + self.get_width()//2, self.get_y() + self.get_height()//2)


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

    topbase = Frame(screen, None, 0, 0,
                        width=screen.get_width(),
                        height=screen.get_height()//2)
    botbase = Frame(screen, None, 0, topbase.get_height(),
                        width=screen.get_width(),
                        height=screen.get_height()//2)
    topframe = Frame(screen, topbase,
                     padx=100, pady=100,
                     bg_color=(255, 0, 0))
    botframe = Frame(screen, botbase,
                     padx=100, pady=100,
                     bg_color=(0, 255, 0))
    subframe = Frame(screen, botframe,
                     padx=50, pady=100,
                     bg_color=(0, 255, 255))

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
