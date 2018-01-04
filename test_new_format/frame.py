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
            assert all(type(x) is int for x in (
                x, y, width, height, padx, pady))
            x += padx
            y += pady
            width -= 2 * padx
            height -= 2 * pady
            self._parent = self
        else:
            assert isinstance(
                parent, Frame), 'parent {} is not Frame()'.format(repr(parent))
            x = parent.get_x() + padx
            y = parent.get_y() + pady
            width = parent.get_width() - 2 * padx
            height = parent.get_height() - 2 * pady
            self._parent = parent
        if width < 0:
            raise ValueError('{}: padx={} too large'.format(
                self.__class__.__name__, padx))
        if height < 0:
            raise ValueError('{}: pady={} too large'.format(
                self.__class__.__name__, pady))
        pygame.Surface.__init__(self, (width, height))
        self._screen = screen
        self.x = x
        self.y = y
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
        pygame.draw.rect(self._screen, self._bg_color,
                         (self._x, self._y, self.get_width(), self.get_height()))

    def _update_position(self) -> None:
        """Update position of Frame based on master, used when drawing."""
        self.set_position(self._parent.get_x() + self._padx,
                          self._parent.get_y() + self._pady)

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
        return (self.get_x() + self.get_width() // 2,
                self.get_y() + self.get_height() // 2)
