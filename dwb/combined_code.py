import pygame
from frame import Frame
from header import Header
from body import Body
from text import TextFrame


import serial
import collections

Reading = collections.namedtuple(
    'Reading', ['mode', 'stable', 'overflow', 'weight', 'units'])


class Scale:
    @staticmethod
    def decode(self, raw: bytes) -> Reading:
        # Handle first byte
        if len(raw) != 6 or raw[0] != 0xff:
            return -1
            # raise ValueError('Not a Global 240878 message')
        # Handle second byte
        decimal_point = raw[1] & 0b111
        current_mode = (raw[1] & 0b11000) >> 3
        negative = (raw[1] & 0b100000) >> 5
        self.stable = (raw[1] & 0b1000000) >> 6
        overflow = (raw[1] & 0b10000000) >> 7
        # TODO: Handle third byte
        digit1 = raw[2] & 0b1111
        digit2 = (raw[2] & 0b11110000) >> 4
        # TODO: Handle fourth byte
        digit3 = raw[3] & 0b1111
        digit4 = (raw[3] & 0b11110000) >> 4
        # TODO: Handle fifth byte
        digit5 = raw[4] & 0b1111
        digit6 = (raw[4] & 0b11110000) >> 4
        # Put it all together
        result = digit1 + (digit2 * 10) + (digit3 * 100) + \
            (digit4 * 1000) + (digit5 * 10000) + (digit6 * 100000)
        result /= 10 ** (decimal_point - 1)
        # Handle sixth byte
        unit = raw[5] & 0b1
        return result

    def __init__(self) -> None:
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)
        self.last_value = 0
        self.stable = 0
        self.original_weight = 0
        self.still_increasing = 0
        self.original_value = 0

    def check(self) -> float:
        """
        Returns a floating point number if scale is measuring something.
        0 means empty scale.
        """
        a = Scale.decode(self, self.ser.read(6))
        if self.stable == 1:
            # min 0.005 increments, unit is lbs
            if (self.last_value + 0.01) < a:
                print("The weight increased")
                difference = a - self.last_value
                self.last_value = a
                return difference

            '''
            if self.last_value == a and self.still_increasing == 1:
                self.still_increasing = 0
                difference = a - self.originnal_value
                return difference  # weight finished rising
            if self.last_value + 0.05 < a and self.still_increasing == 0:
                self.still_increasing = 1
                self.original_value = a  # weight start rising here
            if self.last_value + 0.05 < a and self.still_increasing == 1:
                self.still_increasing = 1  # weight is still rising
            self.last_value = a
            '''
            print("the weight stays the same or decreased")
            self.last_value = a
        return 0  # value stays the same or decreases

    def close(self) -> None:
        self.ser.close()


_DEBUG = False


def _debug_print(*args, **kwargs) -> None:
    if _DEBUG:
        print(*args, **kwargs)


class Display(Frame):
    def __init__(self, header: Header, bodies: [Body], scale):
        Frame.__init__(self, screen, None, 0, 0,
                       screen.get_width(), screen.get_height())
        self._header = header
        self._bodies = bodies
        # Content() to display
        self._last_index = None
        self._curr_index = 0
        # settings for frame position and rotation
        curr_body = self._bodies[self._curr_index]
        self.body_height = sum(body.get_height() for body in curr_body)
        self.y_0 = self._y = -self.body_height
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
        weight = scale.check()
        if weight != 0:
            curr_body = TextFrame(self.screen, self, str(
                weight), text_color=(255, 255, 255))
        else:
            curr_body = self._bodies[self._curr_index]

        if self._stop_y is None or (self._last_index is not None and self._last_index != self._curr_index):
            _debug_print('UPDATE @', self._y, 'last:',
                         self._last_index, 'curr:', self._curr_index)
            self._last_index = self._curr_index  # update last index
            self.body_height = sum(body.get_height() for body in curr_body)
            self.y_0 = self._y = -self.body_height
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
            self.last_index, self._curr_index = self._curr_index, (
                self._curr_index + 1) % len(self._bodies)
        else:
            self.speed_y += self._accel_y  # accelerate image
            self._y += self.speed_y  # change image position by speed amount
            if self._y > self._stop_y and not self._waited:  # set position to stop position if it hasn't waited
                # so it doesn't end up lower that it should when at high speed
                self._y = self._stop_y


if __name__ == '__main__':
    import math
    from mode import Mode
    from pathlib import Path

    from text import TextFrame

    # Display setup values
    FULLSCREEN = True
    FPS = 60
    TEXT_WEIGHT = 1
    CONTENT_WEIGHT = 5
    TEXT_RATIO = TEXT_WEIGHT / (TEXT_WEIGHT + CONTENT_WEIGHT)
    CONTENT_RATIO = 1 - TEXT_RATIO
    CONTENT_PER_FRAME = 2

    # Display modes for each bin
    landfill = Mode('LANDFILL', Path(
        './assets/img/_reduc/_landfill'), (0, 0, 0), (255, 255, 255))
    recycle = Mode('RECYCLE', Path('./assets/img/_reduc/_recycle'),
                   (255, 255, 255), (0, 57, 166))
    compost = Mode('COMPOST', Path('./assets/img/_reduc/_compost'),
                   (255, 255, 255), (21, 161, 25))

    # Determine which mode to use
    while True:
        m = input('L, R, C: ').upper()
        if m == 'L':
            mode = landfill
            break
        elif m == 'R':
            mode = recycle
            break
        elif m == 'C':
            mode = compost
            break

    # Make list of image paths
    image_paths = list(mode.image_path.glob('**/*.png'))

    # Initialize pygame graphical interface
    pygame.init()

    # Display setup
    if FULLSCREEN:
        flags = pygame.FULLSCREEN  # | pygame.DOUBLEBUF | pygame.HWSURFACE
        screen = pygame.display.set_mode((0, 0), flags)
    else:
        screen = pygame.display.set_mode()
    pygame.display.set_caption('Display Test')
    pygame.mouse.set_visible(0)

    # Header
    header_height = int(TEXT_RATIO * screen.get_height())
    header = Header(screen, 0, 0,
                    screen.get_width(), header_height,
                    font_file=str(Path('./assets/fnt/arial-bold.ttf')),
                    text=mode.display_str, text_color=mode.text_color,
                    text_padx=200, text_pady=25,
                    bg_color=mode.bg_color)

    # Body
    frame_count = math.ceil(len(image_paths) / CONTENT_PER_FRAME)

    all_content_height = int(CONTENT_RATIO * screen.get_height())

    body_list = []
    for i in range(frame_count):
        sub_list = []
        # calculate number of content on screen using minimum of desired and remaining images
        content_count = min(CONTENT_PER_FRAME, len(image_paths))
        for j in range(content_count):
            # dynamically adjust content height
            content_height = all_content_height // content_count
            sub_list.append(Body(screen, image_paths.pop(0), 'Testing {}'.format(
                i + j + 1), 0, header.get_height() + j * content_height, screen.get_width(), content_height))
        body_list.append(sub_list)

    # Display
    display = Display(header, body_list, scale_reading)

    # Scale Reading Test
    scale = Scale()
    prev_reading = scale.check()
    scale_reading = TextFrame(
        screen, display, text=str(prev_reading), text_color=(255, 255, 0))

    # FPS
    clock = pygame.time.Clock()
    running = True

    # Animation loop
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

        current_reading = Scale.decode(scale, scale.ser.read(6))
        if scale.stable == 1:
            # min 0.005 increments, unit is lbs
            if (scale.last_value + 0.01) < current_reading:
                print("The weight increased")
                difference = current_reading - scale.last_value
                scale.last_value = current_reading
                scale_reading.set_text(str(difference))
            else:
                scale_reading.set_text(str(0))

            scale.last_value = current_reading
        else:
            scale_reading.set_text(str(0))

            scale.last_value = a
        else:
            scale_reading.set_text(str(0))

        # curr_reading = scale.check()
        # scale_reading.set_text(str(curr_reading))
        # scale_reading.draw()

        clock.tick(FPS)

        pygame.display.flip()

    pygame.quit()
