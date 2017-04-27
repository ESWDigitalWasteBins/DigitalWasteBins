"""
display.py

Description: Display for each screen.

Created on Apr 25, 2017
"""


import pygame
from pygame import font


class Title:
    def __init__(self, text: font.Font, bg: (int)=(0, 0, 0), pady: int=0):
        """
        Title banner for top of Display().

        Args:
            text: title of display
            bg(=(0, 0, 0)): background color for title banner
            pady(=0): padding above and below title text
        """
        self._text = text
        self._bg = bg
        self._pady = pady

    def __str__(self) -> str:
        return 'Title Class: {}'.format(self._text)

    def draw(self, screen: pygame.display) -> None:
        """Blit the title banner to the screen."""
        text_rect = self._text.get_rect()
        width, height = screen.get_size()
        text_height = text_rect.height
        text_rect.midtop = (width/2, self._pady)
        pygame.draw.rect(screen, self._bg, (0, 0, width, text_height + 2*self._pady))
        screen.blit(self._text, text_rect)


# TODO: fill in with animations, etc.
class Content:
    def __init__(self, display_bg_color: (int)=(255, 255, 255)) -> None:
        self._display_bg_color = display_bg_color

    def __str__(self) -> str:
        return 'Content Class'.format()

    def draw(self, screen: pygame.display) -> None:
        screen.fill(self._display_bg_color)


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
        assert type(title) is Title, 'argument title got {}, expected Title()'.format(repr(type(title)))
        self._title = title
        assert type(content) is Content, 'argument title got {}, expected Content()'.format(repr(type(title)))
        self._content = content

    def draw(self, screen, title_weight: int=1, content_weight: int=1) -> None:
        """Draw title and content to screen."""
        self._content.draw(screen)
        self._title.draw(screen)


if __name__ == '__main__':
    from font_manager import FontManager

    BLUE = (0, 57, 166)

    pygame.init()

    screen = pygame.display.set_mode((300, 300))
    pygame.display.set_caption('Display Test')
    title = Title(FontManager().create_text('TEST', 50), bg=BLUE, pady=20)
    content = Content()
    Display(title, content).draw(screen)

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

        clock.tick(20)

        pygame.display.flip()

    pygame.quit()
