import pygame


class TextFrame():
    """Frame for holding text."""
    text_bubble_width = 800
    text_bubble_height = 800

    def __init__(self, screen: pygame.display,
                 text: str='TextFrame', font_file: str or None=None,
                 text_color: (int, int, int)=(0, 0, 0), bg_color: (int, int, int)=(0, 0, 0), width: int=0, height: int=0,
                 padx: int=0, pady: int=0, x: int=0, y: int=0) -> None:

        self.screen = screen
        self.font_size = height
        self.font = pygame.font.Font(font_file, self.font_size)
        self.text_color = text_color
        self.bg_color = bg_color
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        while True:
            self._text = self.font.render(text, True, text_color)
            if self._text.get_width() > width:
                self.font_size -= 10
                self.font = pygame.font.Font(font_file, self.font_size)
            else:
                break
        self._text_rect = self._text.get_rect(center=self.get_center())

    def set_text(self, text: str):
        self._text = self.font.render(text, True, self.text_color)
        self._text_rect = self._text.get_rect(center=self.get_center())

    def draw(self) -> None:
        self._text_rect = self._text.get_rect()
        self.screen.blit(self._text, self._text_rect)

    def get_center(self) -> (int, int):
        """Return 2-tuple of ints representing center (x, y) coordinate."""
        return (self._x + self._width // 2,
                self._y + self._height // 2)

    def draw_text_bubble(self) -> None:
