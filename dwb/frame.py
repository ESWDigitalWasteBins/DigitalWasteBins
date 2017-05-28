import pygame


class BaseFrame(pygame.Surface):
    """BaseFrame class for layout with position and size."""
    def __init__(self, screen: pygame.display,
                 x: int, y: int,
                 width: int, height: int):
        """
        Initialize BaseFrame as subclass of pygame.Surface. Must have
        position and size.

        Args:
            screen: screen to draw on
            x: x-coordinate of top-left corner
            y: y-coordinate of top-left corner
            width: width of frame
            height: height of frame
        """
        pygame.Surface.__init__(self, (width, height))
        self._screen = screen
        self._position = self._x, self._y = (x, y)

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
        return (self.get_x() + self.get_width()//2, self.get_y() + self.get_height()//2)


class Frame(BaseFrame):
    """Frame class for layout with master and padding."""
    def __init__(self, screen: pygame.display, master: BaseFrame or 'Frame',
                 padx: int=0, pady: int=0,
                 bg_color: (int, int, int)=(0, 0, 0)):
        """
        Initialize Frame as subclass of BaseFrame. Must have screen
        to draw on and master for positioning and sizing.

        Args:
            screen: screen to draw on
            master: parent frame of this Frame, either Frame or BaseFrame
            padx(=0): horizontal padding
            pady(=0): vertical padding
            bg_color(=(0, 0, 0)): background color of Frame, a 3-tuple of ints
        """
        x, y = master.get_x() + padx, master.get_y() + pady
        width = master.get_width() - 2*padx
        height = master.get_height() - 2*pady
        BaseFrame.__init__(self, screen, x, y, width, height)
        self._screen = screen
        self._master = master
        self._padx = padx
        self._pady = pady
        self._bg_color = bg_color

    def draw(self) -> None:
        """Draw a rectangle representing this Frame's covering."""
        self._update_position()
        pygame.draw.rect(self._screen, self._bg_color, (self._x, self._y, self.get_width(), self.get_height()))

    def _update_position(self) -> None:
        """Update position of Frame based on master, used when drawing."""
        self._position = self._x, self._y = (self._master.get_x() + self._padx,
                                             self._master.get_y() + self._pady)


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

    topbase = BaseFrame(screen, 0, 0,
                        width=screen.get_width(),
                        height=screen.get_height()//2)
    botbase = BaseFrame(screen, 0, topbase.get_height(),
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
