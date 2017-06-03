"""
display.py

Description: Display for each screen.

Created on Apr 25, 2017
"""


import pygame
from pathlib import Path
from frame import Frame, BaseFrame


data_dir = Path.cwd() / 'test' / 'images'


def load_image(name, colorkey=None):
    fullname = str(data_dir / name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image:', fullname)
        raise SystemExit(str(pygame.compat.geterror()))
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image  # , image.get_rect()


def scale_image(image: pygame.image, size: (int, int)) -> pygame.image:
    width, height = size
    iwidth, iheight = image.get_size()  # image dimensions
    scale_y = height / iheight          # scale by height
    scale_x = width / iwidth            # scale by width
    scale = min(scale_x, scale_y)       # scale by the smaller value
    if scale > 1:
        scale = 1
    return pygame.transform.scale(image, (int(scale*iwidth), int(scale*iheight)))


class TextFrame(Frame):
    def __init__(self, screen: pygame.display, master: Frame, text: str, padx: int=0, pady: int=0):
        Frame.__init__(self, screen, master)
        self._text = text
        self._padx, self._pady = padx, pady

    def draw(self) -> None:
        self.update_position()
        font = pygame.font.Font(None, self.set_font_size())
        text = font.render(self._text, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.midtop = (self._parent.get_width()//2, self._pady)
        self._screen.blit(text, text_rect)

    # TODO: determine how to do
    def set_font_size(self):
        return 50


class TitleFrame(Frame):
    """[SUMMARY]"""
    def __init__(self, screen: pygame.display, master: BaseFrame, text: str, bg_color: (int)=(0, 0, 0), text_pady: int=0):
        """
        Title banner for top of Display().

        Args:
            text: title of display
            bg(=(0, 0, 0)): background color for title banner
            pady(=0): padding above and below title text
        """
        Frame.__init__(self, screen, master, bg_color=bg_color)
        self._text_frame = TextFrame(self._screen, self, text, pady=text_pady)
        print(self._size)

    def draw(self) -> None:
        """Blit the title frame to the screen."""
        self.update_position()
        pygame.draw.rect(self._screen, self._bg_color, (self._x, self._y, self._width, self._height))
        # text_rect = self._text.get_rect()
        # text_height = text_rect.height
        # text_rect.midtop = (self._width/2, self._pady)
        # self._screen.blit(self._text, text_rect)
        self._text_frame.draw()


class InfoFrame(Frame):
    def __init__(self, screen: pygame.display, master: Frame, image_path: str, text: str, *args, **kwargs):
        Frame.__init__(self, screen, master, *args, **kwargs)
        self._image_path = image_path
        self._text = text

    # def draw(self) -> None:
    #     pass

    def get_image_path(self) -> str:
        return self._image_path

    def get_text(self) -> str:
        return self._text


class DisplayFrame(Frame):
    def __init__(self, screen: pygame.display, content: [InfoFrame], bg_color: (int)=(255, 255, 255), *args, **kwargs):
        Frame.__init__(self, screen, bg_color, args, kwargs)
        self.content = content
        self.bg_color = bg_color
        self._cache = {}  # stores each panel's rendered text and rendered image

    # def draw(self, screen: pygame.display, padx: int=0, pady: int=0) -> None:
    #     screen.fill(self.bg_color)
    #     pad_width, pad_height = screen.get_width() - 2*padx, screen.get_height() - 2*pady
    #     info_frame_y = pady
    #     for i, info_frame in enumerate(self.content):
    #         info_frame_width, info_frame_height = pad_width, pad_height // len(self.content)
    #         self.draw_info_frame(screen, info_frame, self._x + padx, self._y + info_frame_y, info_frame_width, info_frame_height, pady=20, padtexty=10)
    #         info_frame_y += screen.get_height() // len(self.content)

    # def draw_info_frame(self, screen: pygame.display, info_frame: InfoFrame,
    #                     x: int, y: int,
    #                     width: int, height: int,
    #                     padx: int=0, pady: int=0,
    #                     padtexty: int=0) -> None:
    #     # width, height = screen.get_size()
    #     if info_frame not in self._cache:
    #         self._cache[info_frame] = {}
    #         self._cache[info_frame]['text'] = pygame.font.SysFont('', 36).render(info_frame.get_caption(), True, (255, 255, 255))
    #         iwidth = width - 2*padx
    #         iheight = height - 2*pady - padtexty - self._cache[info_frame]['text'].get_height()
    #         self._cache[info_frame]['image'] = scale_image(load_image(info_frame.get_image_path()), (iwidth, iheight))
    #     image_rect = self._cache[info_frame]['image'].get_rect(midtop=(x + width//2, y + pady))
    #     screen.blit(self._cache[info_frame]['image'], image_rect)
    #     iheight = self._cache[info_frame]['image'].get_height()
    #     text_rect = self._cache[info_frame]['text'].get_rect(midtop=(x + width//2, y + padtexty + iheight))
    #     screen.blit(self._cache[info_frame]['text'], text_rect)


# def make_frames(screen) -> [DisplayFrame]:
#     all_content = [InfoFrame(screen, str(path), str(path)) for path in data_dir.glob('**/*.png')]
#     f1 = DisplayFrame(screen, all_content[:3], bg_color=(0, 0, 0))
#     f2 = DisplayFrame(screen, all_content[3:6], bg_color=(0, 0, 0))
#     f3 = DisplayFrame(screen, all_content[6:8], bg_color=(0, 0, 0))
#     return [f1, f2, f3]


# TODO: fill in with animations, etc.
class Content:
    """[SUMMARY]"""
    def __init__(self, screen, content_base) -> None:
        """
        Content animations below Title() banner in Display().

        Args:
            title: Title() banner at top of screen
            content: Content() for screen

        Attributes:
            [ATTR1]: [DESCRIPTION]
            [ATTR2]: [DESCRIPTION]
        """
        self._screen = screen
        self._content_base = content_base
        self.width, self.height = self._content_base.get_size()
        # frames to display
        self.display_frames = [InfoFrame(self._screen, self._content_base, 'images\\items\\1.png', 'Test')]  # make_frames(self.screen)
        self.last_index = None
        self.curr_index = 0
        # settings for frame position and rotation
        self.y_0 = self.y = -self._content_base.get_height()
        self.stop_y = None  # stop y position for images
        self.waited = False
        self.waiting = False
        self.time_start = None
        self.time_now = pygame.time.get_ticks()
        self.wait_time = 1000  # in milliseconds
        # physics
        self.speed_0_y = self.speed_y = 0  # initial speed and current speed
        self.accel_y = 0.7*self.height/1080  # acceleration of falling images

    def __str__(self) -> str:
        return 'Content Class'.format()

    def draw(self) -> None:
        """Blit content animations to screen."""
        if self.stop_y is None or (self.last_index is not None and self.last_index != self.curr_index):
            print('UPDATE @', self.y, 'last:', self.last_index, 'curr:', self.curr_index)
            self.last_index = self.curr_index  # update last index
            self.y_0 = self.y = -self._ce.get_height()
            self.stop_y = (self.height - self._screen.get_height()) // 2
        self.draw_frame()
        # check if image has waited specified amount of time
        if not self.waited and not self.waiting and self.y >= self.stop_y:
            print('STOP @', self.y)
            self.time_start = pygame.time.get_ticks()
            self.waiting = True
        self.time_now = pygame.time.get_ticks()
        if self.waiting and self.time_start and (self.time_now - self.time_start) >= self.wait_time:
            self.waited = True
            self.waiting = False
            self.speed_y = self.speed_0_y  # reset speed to initial speed
        # Update y position only if not waiting
        if not self.waiting:
            self.update_y_position()

    def draw_frame(self):
        """Draw Frame onto screen at y position."""
        self.display_frames[self.curr_index].set_position(0, self.y)
        self.display_frames[self.curr_index].draw()

    def update_y_position(self):
        width, height = self._screen.get_size()
        if self.y >= height:
            print('NEXT @', self.y)
            self.y = self.y_0  # move image back to top
            self.waited = False  # after pausing for specified time
            # cycle through image indexes
            self.last_index, self.curr_index = self.curr_index, (self.curr_index + 1) % len(self.display_frames)
        else:
            self.speed_y += self.accel_y  # accelerate image
            self.y += self.speed_y  # change image position by speed amount


class Display:
    """[SUMMARY]"""
    def __init__(self, screen, title_base: BaseFrame, title: TitleFrame, content_base: BaseFrame, content: Content):
        """
        Display for a single screen.

        Args:
            title: Title() banner at top of screen
            content: Content() for screen

        Attributes:
            [ATTR1]: [DESCRIPTION]
            [ATTR2]: [DESCRIPTION]
        """
        self._title_base = title_base
        self._title = title
        self._content_base = content_base
        self._content = content
        self.mode = 0  # 0 regular, 1 reaction

    def draw(self, screen, title_weight: int=1, content_weight: int=1) -> None:
        """Draw title and content to screen."""
        self._content.draw()
        self._title.draw()


# Testing
if __name__ == '__main__':
    BLUE = (0, 57, 166)

    pygame.init()
    # screen = pygame.display.set_mode((350, 700))
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('Display Test')

    title_base = BaseFrame(screen, x=0, y=0, width=screen.get_width(), height=int(screen.get_height()*.10))
    content_base = BaseFrame(screen, x=0, y=0, width=screen.get_width(), height=screen.get_height() - title_base.get_height())

    title = TitleFrame(screen, title_base, 'This is a Title', bg_color=BLUE, text_pady=20)
    content = Content(screen, content_base)
    display = Display(screen, title_base, title, content_base, content)

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

        display.draw(screen)

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()
