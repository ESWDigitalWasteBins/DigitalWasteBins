"""
display.py

Description: Display for each screen.

Created on Apr 25, 2017
"""


import pygame
from pygame import font


class Title:
    """[SUMMARY]"""
    def __init__(self, text: font.Font, bg: (int)=(0, 0, 0), pady: int=0):
        """
        Title banner for top of Display().

        Args:
            text: title of display
            bg(=(0, 0, 0)): background color for title banner
            pady(=0): padding above and below title text
        """
        self.text = text
        self.bg = bg
        self.pady = pady

    def __str__(self) -> str:
        return 'Title Class: {}'.format(self.text)

    def draw(self, screen) -> None:
        """Blit the title banner to the screen."""
        text_rect = self.text.get_rect()
        width, height = screen.get_size()
        text_height = text_rect.height
        text_rect.midtop = (width/2, self.pady)
        pygame.draw.rect(screen, self.bg, (0, 0, width, text_height + 2*self.pady))
        screen.blit(self.text, text_rect)


class Frame:
    def __init__(self):
        self.surfaces = {}
        self.y = 0
        self.bg_color = (255, 255, 255)

    def set_position(self, y: int) -> None:
        self.y = y

    def draw(self, screen) -> None:
        screen.fill(self.bg_color)
        text = pygame.font.Font(None, 100).render('Test', True, (0, 0, 0))
        self.surfaces['text'] = text
        screen.blit(text, (0, self.y))

    def get_height(self) -> int:
        assert all(type(surface) == pygame.Surface for surface in self.surfaces.values())
        return sum(surface.get_height() for surface in self.surfaces.values())


# TODO: fill in with animations, etc.
class Content:
    """[SUMMARY]"""
    def __init__(self) -> None:
        """
        Content animations below Title() banner in Display().

        Args:
            title: Title() banner at top of screen
            content: Content() for screen

        Attributes:
            [ATTR1]: [DESCRIPTION]
            [ATTR2]: [DESCRIPTION]
        """
        # frames to display
        self.frames = [Frame(), Frame(), Frame()]
        self.last_index = None
        self.curr_index = 0
        # settings for frame position and rotation
        self.y_0 = self.y = -self.frames[self.curr_index].get_height()
        self.stop_y = None  # stop y position for images
        self.waited = False
        self.waiting = False
        self.time_start = None
        self.time_now = pygame.time.get_ticks()
        self.wait_time = 1000  # in milliseconds
        # physics
        self.speed_0_y = self.speed_y = 0  # initial speed and current speed
        self.accel_y = 0.2  # acceleration of falling images

    def __str__(self) -> str:
        return 'Content Class'.format()

    def draw(self, screen) -> None:
        """Blit content animations to screen."""
        width, height = screen.get_size()
        if not self.stop_y or self.last_index is not None and self.last_index != self.curr_index:
            print('UPDATE @', self.y, 'last:', self.last_index, 'curr:', self.curr_index)
            self.last_index = self.curr_index  # update last index
            self.y_0 = self.y = -self.frames[self.curr_index].get_height()
            self.stop_y = (height - self.frames[self.curr_index].get_height()) // 2
        self.draw_frame(screen)
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
            self.update_y_position(screen)

    def draw_frame(self, screen):
        """Draw Frame onto screen at y position."""
        self.frames[self.curr_index].set_position(self.y)
        self.frames[self.curr_index].draw(screen)

    def update_y_position(self, screen):
        width, height = screen.get_size()
        if self.y >= height:
            print('NEXT @', self.y)
            self.y = self.y_0  # move image back to top
            self.waited = False  # after pausing for specified time
            # cycle through image indexes
            self.last_index, self.curr_index = self.curr_index, (self.curr_index + 1) % len(self.frames)
        else:
            self.speed_y += self.accel_y  # accelerate image
            self.y += self.speed_y  # change image position by speed amount


class Display:
    """[SUMMARY]"""
    def __init__(self, title: Title, content: Content):
        """
        Display for a single screen.

        Args:
            title: Title() banner at top of screen
            content: Content() for screen

        Attributes:
            [ATTR1]: [DESCRIPTION]
            [ATTR2]: [DESCRIPTION]
        """
        assert type(title) is Title, 'argument title got {}, ' \
            'expected Title()'.format(repr(type(title)))
        self.title = title
        assert type(content) is Content, 'argument title got {}, ' \
            'expected Content()'.format(repr(type(title)))
        self.content = content
        self.mode = 0  # 0 regular, 1 reaction

    def draw(self, screen, title_weight: int=1, content_weight: int=1) -> None:
        """Draw title and content to screen."""
        self.content.draw(screen)
        self.title.draw(screen)


# Testing
if __name__ == '__main__':
    from font_manager import FontManager

    BLUE = (0, 57, 166)

    pygame.init()
    screen = pygame.display.set_mode((350, 700))
    pygame.display.set_caption('Display Test')

    title = Title(FontManager().create_text('TEST', 50), bg=BLUE, pady=20)
    content = Content()
    display = Display(title, content)

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
