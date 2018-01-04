import pygame
from pygame.locals import *

# contain the functions to draw each sector
# of the screen


class text_surface:
    def __init__(self, screen: pygame.surface, surface_image: pygame.surface, line_number: int=4, top_offset: int=0, bot_offset: int=0, left_offset: int=0, right_offset: int=0, color: (int, int, int)=(0, 0, 0), font: str="")->None:
        self._font = pygame.font.SysFont('Calibri', 70, True)
        self._height = self._font.get_height()
        self._size_per_line = self._font.get_linesize()
        self._surface_width = surface_image.get_size()

        self._screen = screen
        self._surface = surface_image
        self._color = color
        self._line_number = line_number

        self.line_list_rect_stored = []
        for counter in range(0, line_number):
            self.line_list_rect_stored.append(pygame.Rect(
                left_offset, top_offset + counter * self._size_per_line, self._surface_width, self._height))

    def draw_text_surface(self, line_list: []) ->None:
        """draw text on a saved surface"""
        self._screen.fill((255, 255, 255))
        counter = 0
        tx_font = self._font
        tx_color = self._color
        for i in line_list:
            self._screen.blit(tx_font.render(i, True, tx_color),
                              self.line_list_rect_stored[counter])
            counter += 1
        self._screen.pygame.display.flip()


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
# possible mode to be 'l', 'c', 'r'


def compost_text_processing(ounces_recycled: int=0):
    processed_text = []
    energy_conversion = 0.3968316
    processed_text.append("Thank you for composting!")
    processed_text.append("You just composted " +
                          str(ounces_recycled) + " ounces")
    processed_text.append("You just helped avoid " + str(ounces_recycled *
                                                         energy_conversion) + " ounces of carbone-equivalent emissions!")
    processed_text.append(
        "Food waste is the single largest part of waste. Keeping it out of landfills is important!")
    return processed_text


def recycle_text_processing(ounces_recycled: int=0):
    energy_conversion = 3.1526066
    processed_text = []
    processed_text.append("Thank you for recycling")
    processed_text.append("You just composted " +
                          str(ounces_recycled) + " ounces")
    processed_text.append("You just helped avoid " +
                          str(ounces_recycled * energy_conversion) + " ounces")


def landfill_text_processing(ounces_recycled: int=0):
    processed_text = []
    processed_text.append(
        "It’s important to separate items that can’t be composted or recycled. Thank you!")
    processed_text.append(
        "Keeping landfill waste in the landfill bins allows other waste to be truly composted and recycled!")
    processed_text.append(
        "Keeping landfill items out of compost and recycling is important. Thank you!")
