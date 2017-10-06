import pygame


class Frame(pygame.Surface):
    """Frame class for layout with position and size."""

    def __init__(self, screen: pygame.display, parent: 'Frame' or None=None,
                 x: int=0, y: int=0,
                 width: int=0, height: int=0,
                 padx: int=0, pady: int=0,
                 bg_color: (int, int, int)=(255, 255, 255)):
        """Initialize Frame as subclass of pygame.Surface.

        Must have a master or position and size based on screen.

        Args:
            screen: screen to draw on
            master(=None): master Frame that determines this Frame's positioning or None to take screen size
            x(=0): x-coordinate of top-left corner
            y(=0): y-coordinate of top-left corner
            width(=None): width of frame
            height(=None): height of frame
            padx(=0): horizontal padding
            pady(=0): vertical padding
            bg_color(=(0, 0, 0)): background color of Frame, a 3-tuple of ints
        """
        if parent is None:
            assert all(type(x) is int for x in (x, y, width, height, padx, pady))
            x += padx
            y += pady
            width -= 2*padx
            height -= 2*pady
            self._parent = self
        else:
            assert isinstance(parent, Frame), 'master is not Frame()'
            x = parent.get_x() + padx
            y = parent.get_y() + pady
            width = parent.get_width() - 2*padx
            height = parent.get_height() - 2*pady
            self._parent = parent
        if width < 0:
            raise ValueError('{}: padx={} too large'.format(self.__class__.__name__, padx))
        if height < 0:
            raise ValueError('{}: pady={} too large'.format(self.__class__.__name__, pady))
        pygame.Surface.__init__(self, (width, height))
        self._screen = screen
        self.set_position(x, y)
        self._padx = padx
        self._pady = pady
        self._bg_color = bg_color

    def __str__(self) -> str:
        """Return string representation of Frame()."""
        s = '{}(parent={}, x={}, y={}, width={}, height={}, padx={}, pady={})'
        return s.format(self.__class__.__name__,
                        'self' if self._parent is self else self._parent.__class__.__name__,
                        self.get_x(), self.get_y(),
                        self.get_width(), self.get_height(),
                        self._padx, self._pady)

    def draw(self) -> None:
        """Draw a rectangle representing this Frame's covering."""
        self._update_position()
        pygame.draw.rect(self._screen, self._bg_color, (self._x, self._y, self.get_width(), self.get_height()))

    def _update_position(self) -> None:
        """Update position of Frame based on master, used when drawing."""
        self.set_position(self._parent.get_x() + self._padx,
                          self._parent.get_y() + self._pady)

    def set_position(self, x: int=None, y: int=None) -> None:
        """Set frame's top-left coordinate, unchanged if not specified.

        Args:
            x(=None): set frame's top-left x coordinate
            y(=None): set frame's top-left y coordinate
        """
        if x is not None:
            self._x = x
        if y is not None:
            self._y = y
        self._position = (self._x, self._y)

    def change_position(self, dx: int=None, dy: int=None) -> None:
        """Change frame's top-left coordinate, unchanged if not specified.

        Args:
            dx(=None): change frame's top-left x coordinate
            dy(=None): change frame's top-left y coordinate
        """
        if dx is not None:
            self._x += dx
        if dy is not None:
            self._y += dy
        self._position = (self._x, self._y)

    def get_x(self) -> int:
        """Return top-left x coordinate."""
        return self._x

    def get_y(self) -> int:
        """Return top-left y coordinate."""
        return self._y

    def get_position(self) -> (int, int):
        """Return 2-tuple of ints representing top-left (x, y) coordinate."""
        return self._position

    def get_center(self) -> (int, int):
        """Return 2-tuple of ints representing center (x, y) coordinate."""
        return (self.get_x() + self.get_width()//2,
                self.get_y() + self.get_height()//2)


# Test Frame
if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('Frame Test')
    pygame.mouse.set_visible(0)

    running = True
    clock = pygame.time.Clock()

    topbase = Frame(screen, None, 0, 0,
                        width=screen.get_width(),
                        height=screen.get_height()//2,
                        padx=100, pady=100)
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

        topbase.set_position(y=y)
        botbase.set_position(y=y + topbase.get_height())

        topframe.draw()
        botframe.draw()
        subframe.draw()

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()
