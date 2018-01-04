import pygame
from pygame.locals import *

# contain the functions to draw each sector
# of the screen


def draw_one_sector(screen, sec_rectange, list_legnth, l, list_rect, square_length, FPS, im)->None:
    white = (255, 255, 255)
    black = (0, 0, 0)
    clock1 = pygame.time.Clock()
    screen.fill((white), sec_rectange)
    for (i, j) in zip(range(0, list_legnth), range(0, list_legnth)):
        for(k, v) in zip(range(0, i + 1), range(0, j + 1)):
            screen.blit(im[l], list_rect[k * list_legnth + j], (k *
                                                                square_length, j * square_length, square_length, square_length))
            screen.blit(im[l], list_rect[i * list_legnth + v], (i *
                                                                square_length, v * square_length, square_length, square_length))

            pygame.display.flip()

        clock1.tick(FPS)


class text_surface():
    def __init__(self, screen: pygame.surface, surface_image: pygame.surface, line_list: [], top_offset: int=0, bot_offset: int=0, left_offset: int=0, right_offset: int=0, color: (int, int, int)=(0, 0, 0), font: str="")->None:
        self._font = pygame.font.SysFont('Calibri', 70, True)
        self._height = font.get_height()
        self._size_per_line = font.get_linesize()
        self._surface_width = surface_image.get_size()

        self._screen = screen
        self._surface = surface_image
        self._color = color
        self._line_number = len(line_list)
        counter = 0
        self.line_list_rect_stored = []
        self.line_list_text_stored = []
        for i in line_list:
            self.line_list_rect_stored.append(pygame.Rect(
                left_offset, top_offset + counter * self._size_per_line, self._surface_width, self._height))
            self.line_list_text_stored.append(
                font.render(i, True, self._color))
            counter += 1

    def draw_text_bubble(self) ->None:
        """draw text on a saved surface"""
        for i in range(0, self._line_number):
            self._screen.blit(self.line_list_text_stored[i],
                              self.line_list_rect_stored[i])
        self._screen.pygame.display.flip()
