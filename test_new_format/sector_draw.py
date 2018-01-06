import pygame
from pygame.locals import *

# contain the functions to draw each sector
# of the screen

white = (255, 255, 255)
black = (0, 0, 0)


class text_surface:
    def __init__(self, screen, surface_image: pygame.surface, line_number: int=4, left_offset: int=0, top_offset: int=0,  tx_color: (int, int, int)=(0, 0, 0), type_font: str="",  bg_color=None, isheader=False):

        self._bg_color = bg_color
        self._font = pygame.font.SysFont('Calibri', 70, True)
        self._height = self._font.get_height()
        self._size_per_line = (self._font).get_linesize()
        self._surface_width = surface_image.get_width()
        self._screen = screen
        self._surface = surface_image
        self._txcolor = tx_color
        self._line_number = line_number
        self._top_offset = top_offset
        self._left_offset = left_offset
        self.line_list_rect_stored = []
        self._isheader = isheader
        for counter in range(0, line_number):
            (self.line_list_rect_stored).append(pygame.Rect(
                left_offset, top_offset + counter * (self._size_per_line), self._surface_width, self._height))

    def draw_text_surface(self, line_list: []) ->None:
        """draw text on a saved surface"""

        if not(self._isheader):
            # load the image of the textbox
            self._screen.blit(self._surface, (0, 0))
        else:
            self._screen.fill((self._bg_color), (0, self._top_offset,
                                                 self._surface_width, self._size_per_line * self._line_number))
        counter = 0
        tx_font = self._font
        tx_color = self._txcolor
        for i in line_list:

            self._screen.blit(tx_font.render(i, True, tx_color, self._bg_color),
                              self.line_list_rect_stored[counter])
            counter += 1
        pygame.display.flip()


def draw_one_sector(screen, sec_rectange, list_length_vertical, list_length_horizontal, l, list_rect, square_length, FPS, im, headroom: int=0)->None:
    white = (255, 255, 255)
    black = (0, 0, 0)
    clock1 = pygame.time.Clock()
    screen.fill((white), sec_rectange)

    for i in range(0, list_length_horizontal):
        for j in range(0, list_length_vertical):
            for k in range(0, i + 1):
                screen.blit(im[l], list_rect[k * list_length_vertical + j], (k *
                                                                             (square_length), j * square_length, square_length, square_length))
            for v in range(0, j + 1):
                screen.blit(im[l], list_rect[i * list_length_vertical + v], (i *
                                                                             (square_length + headroom), v * square_length, square_length, square_length))
    pygame.display.flip()

# possible mode to be 'l', 'c', 'r'


def compost_text_processing(ounces_recycled: int=0):
    processed_text = []
    energy_conversion = 0.3968316
    processed_text.append("Thank you for composting!")
    processed_text.append("You just composted " +
                          str(round(ounces_recycled, 3)) + " ounces")
    processed_text.append("You just helped avoid " + str(round(ounces_recycled *
                                                               energy_conversion, 3)) + " ounces")
    processed_text.append(" of CO2e")
    processed_text.append(
        "Food waste is the single largest part of waste.")
    processed_text.append("Keeping it out of landfills is important!")
    return processed_text


def recycle_text_processing(ounces_recycled: int = 0):
    energy_conversion = 3.1526066
    processed_text = []
    processed_text.append("Thank you for recycling")
    processed_text.append("You just composted " +
                          str(round(ounces_recycled, 3)) + " ounces")
    processed_text.append("You just helped avoid " +
                          str(round(ounces_recycled *
                                    energy_conversion, 3)) + " ounces")


def landfill_text_processing(ounces_recycled: int = 0):
    processed_text = []
    processed_text.append(
        "It’s important to separate items that can’t be composted or recycled.")
    processed_text.append("Thank you!")
    processed_text.append(
        "Keeping landfill waste in the landfill bins allows other")
    processed_text.append("waste to be truly composted and recycled!")
    processed_text.append(
        "Keeping landfill items out of compost and recycling is important.")
    processed_text.append("Thank you!")
