import pygame
import images
from frame import Frame


_DEBUG = True


def _debug_print(*args, **kwargs) -> None:
    if _DEBUG:
        print(*args, **kwargs)


class TextFrame(Frame):
    def __init__(self, screen: pygame.display, parent: Frame,
                 text: str, padx: int=0, pady: int=0) -> None:
        Frame.__init__(self, screen, parent, padx, pady)
        self._text = text

    def draw(self) -> None:
        self._update_position()
        font = pygame.font.Font(None, self.get_height())
        text = font.render(self._text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.get_center())
        self._screen.blit(text, text_rect)


class Header(Frame):
    def __init__(self, screen: pygame.display,
                 x: int, y: int, width: int, height: int,
                 text: str, bg_color: (int, int, int)=(0, 0, 0)) -> None:
        Frame.__init__(self, screen, None, x, y, width, height)
        self._bg_color = bg_color
        self._text_frame = TextFrame(screen, self, text)

    def draw(self) -> None:
        pygame.draw.rect(self._screen, self._bg_color, (self.get_x(), self.get_y(), self.get_width(), self.get_height()))
        self._text_frame.draw()


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
        self._image = images.scale_image(images.load_image(image_path), isize)
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
        self._content = Content(screen, self, image_path, text, content_padx=20, content_pady=50)

    def draw(self):
        self._content.draw()


class Display(Frame):
    def __init__(self, header: Header, bodies: [Body]):
        Frame.__init__(self, screen, None, 0, 0, screen.get_width(), screen.get_height())
        self._header = header
        self._bodies = bodies
        # Content() to display
        self._last_index = None
        self._curr_index = 0
        # settings for frame position and rotation
        curr_body = self._bodies[self._curr_index]
        body_height = sum(body.get_height() for body in curr_body)
        self.y_0 = self._y = -body_height
        self._stop_y = self._header.get_height()  # stop y position for images
        self._waited = False
        self._waiting = False
        self._time_start = None
        self._time_now = pygame.time.get_ticks()
        self._wait_time = 1000  # in milliseconds
        # physics
        self.speed_0_y = self.speed_y = 0  # initial speed and current speed
        self._accel_y = 0.7  # acceleration of falling images

    def draw(self):
        """Blit animations to screen."""
        self._screen.fill((0, 0, 0))
        curr_body = self._bodies[self._curr_index]
        body_height = sum(body.get_height() for body in curr_body)
        if self._stop_y is None or (self._last_index is not None and self._last_index != self._curr_index):
            _debug_print('UPDATE @', self._y, 'last:', self._last_index, 'curr:', self._curr_index)
            self._last_index = self._curr_index  # update last index
            self.y_0 = self._y = -body_height
            # self._stop_y = (body_height - self.get_height()) // 2
        self._draw_body()
        # check if image has waited specified amount of time
        if not self._waited and not self._waiting and self._y >= self._stop_y:
            _debug_print('STOP @', self._y)
            self._time_start = pygame.time.get_ticks()
            self._waiting = True
        self._time_now = pygame.time.get_ticks()
        if self._waiting and self._time_start and (self._time_now - self._time_start) >= self._wait_time:
            self._waited = True
            self._waiting = False
            self.speed_y = self.speed_0_y  # reset speed to initial speed
        # Update y position only if not waiting
        if not self._waiting:
            self._update_y_position()
        self._header.draw()

    def _draw_body(self):
        """Draw Body onto screen at y position."""
        # _debug_print('DRAW @', self._y)
        curr_body = self._bodies[self._curr_index]
        curr_y = self.get_y()
        for i in range(len(curr_body)):
            curr_body[i].set_position(0, curr_y)
            curr_y += curr_body[i].get_height()
            curr_body[i].draw()

    def _update_y_position(self):
        if self._y >= self.get_height():
            _debug_print('NEXT @', self._y)
            self._y = self.y_0  # move image back to top
            self._waited = False  # after pausing for specified time
            # cycle through image indexes
            self.last_index, self._curr_index = self._curr_index, (self._curr_index + 1) % len(self._bodies)
        else:
            self.speed_y += self._accel_y  # accelerate image
            self._y += self.speed_y  # change image position by speed amount
            if self._y > self._stop_y and not self._waited:  # set position to stop position if it hasn't waited
                self._y = self._stop_y                       # so it doesn't end up lower that it should when at high speed


if __name__ == '__main__':
    TEXT_WEIGHT = 1
    CONTENT_WEIGHT = 5
    TEXT_RATIO = TEXT_WEIGHT / (TEXT_WEIGHT + CONTENT_WEIGHT)
    CONTENT_RATIO = 1 - TEXT_RATIO

    BLUE = (0, 57, 166)

    pygame.init()
    flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
    screen = pygame.display.set_mode((0, 0), flags)
    pygame.display.set_caption('Display Test')

    header_height = int(TEXT_RATIO*screen.get_height())
    header = Header(screen, 0, 0,
                    screen.get_width(), header_height,
                    'RECYCLE', BLUE)

    frame_count = 5
    content_per_frame = 2

    all_content_height = int(CONTENT_RATIO*screen.get_height())
    body_height = all_content_height // content_per_frame

    body_list = []
    for i in range(frame_count):
        sub_list = []
        for j in range(content_per_frame):
            print(header.get_height() + j*body_height)
            sub_list.append(Body(screen, 'images\\items\\{}.png'.format(i+j+1), 'Testing {}'.format(i+j+1), 0, header.get_height() + j*body_height, screen.get_width(), body_height))
        body_list.append(sub_list)

    display = Display(header, body_list)

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

        screen.fill((0, 0, 0))
        display.draw()

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()
