import pygame
from frame import Frame
from header import Header
from body import Body

from collections import namedtuple

from scale import Scale

from stopwatch import Stopwatch

Reading = namedtuple(
    'Reading', ['mode', 'stable', 'overflow', 'weight', 'units'])


_DEBUG = False


sw = Stopwatch()
sw_global = Stopwatch()
log = open("debug.log", "w")


def _debug_print(*args, **kwargs) -> None:
    if _DEBUG:
        print(*args, **kwargs)


def _sw_log(log: "file", time_type, sw: Stopwatch) -> None:
    log.write("TIME (" + time_type + "): " + str(sw.read()) + "\n")


class Display(Frame):
    def __init__(self, header: Header, bodies: [Body]):
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
    sw_global.start()
    _sw_log(log, "BEGIN GLOBAL", sw_global)

    import math
    from mode import Mode
    from pathlib import Path

    from text import TextFrame

    # Display setup values
    FULLSCREEN = True
    FPS = 30
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
            energy_conversion = 1  # no specific conversion factor for landfill
            mode = landfill
            break
        elif m == 'R':
            energy_conversion = 3.1526066
            mode = recycle
            break
        elif m == 'C':
            energy_conversion = 0.3968316
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
    display = Display(header, body_list)

    # Scale Reading Test
    my_scale = Scale()
    #prev_reading = my_scale.check()
    scale_reading = TextFrame(
        screen, display, text=str(prev_reading), text_color=(255, 255, 0))

    # FPS
    clock = pygame.time.Clock()
    running = True

    # Scale
    SCALEREADEVENT = pygame.USEREVENT + 1
    SCALEREADTIME = 200  # milliseconds
    pygame.time.set_timer(SCALEREADEVENT, SCALEREADTIME)

    _sw_log(log, "GLOBAL", sw_global)
    # Animation loop
    while running:
        _sw_log(log, "GLOBAL", sw_global)
        sw.reset()
        sw.start()
        _sw_log(log, "begin while", sw)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
            elif event.type == SCALEREADEVENT:
                if my_scale.ser.in_waiting > 0:
                    reading = my_scale.ser.read(6)
                    # unit should be converted to ounces
                    weight = my_scale.check(reading)

                    energy_saved = weight * energy_conversion  # unit is ounces of carbon emission
                    _sw_log(log, "scale " + str(weight), sw)
                    # if weight != 0:
                    # display.is_using_scale = True
                    scale_reading.set_text(format(weight, '.5f'))  # 5 decimals
                    # elif display.frame_type == 1:
                    # display.is_using_scale=False

        screen.fill((0, 0, 0))
        _sw_log(log, "fill", sw)

        display.draw()
        _sw_log(log, "draw", sw)

        # curr_reading = scale.check()
        # scale_reading.set_text(str(curr_reading))
        scale_reading.draw()

        clock.tick(FPS)
        _sw_log(log, "clock tick", sw)

        pygame.display.flip()
        _sw_log(log, "end while", sw)

    pygame.quit()

    _sw_log(log, "END GLOBAL", sw_global)

    log.close()
