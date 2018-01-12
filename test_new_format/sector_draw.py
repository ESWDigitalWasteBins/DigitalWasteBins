import pygame
from pygame.locals import *

# contain the functions to draw each sector
# of the screen

white = (255, 255, 255)
black = (0, 0, 0)


class text_surface:
    def __init__(self, screen, surface_image: pygame.surface, line_number: int=4, left_offset: int=0, top_offset: int=0, surface_left_offset: int=0, surface_top_offset: int=0, tx_color: (int, int, int)=(0, 0, 0), type_font: str="",  bg_color=None, isheader=False):

        # background color to draw text on
        self._bg_color = bg_color
        font_size = 80 if isheader else 60
        self._font = pygame.font.Font(
            './test_new_format/Font_Folder/Chivo/Chivo-Black.ttf', font_size)
        if isheader:
            self._size_per_line = (self._font).get_descent() - 10
        else:
            self._size_per_line = (self._font).get_linesize()
        # 60 seems good for text box, 80 for headers
        #self._height = self._font.get_height()

        self._surface_width = surface_image.get_width()
        self._screen = screen
        self._surface = surface_image
        self._txcolor = tx_color
        self._line_number = line_number

        # used to offset characters
        self._top_offset = top_offset
        self._left_offset = left_offset

        # rectange to draw on
        self.line_list_rect_stored = []

        self._isheader = isheader

        # used for text bubble adjustment
        self._surface_top_offset = surface_top_offset
        self._surface_left_offset = surface_left_offset

        for counter in range(0, line_number):
            (self.line_list_rect_stored).append(pygame.Rect(
                left_offset, top_offset + counter * (self._size_per_line), self._surface_width, self._size_per_line))
            pygame.event.pump()

    def draw_text_surface(self, line_list: []) ->None:
        """draw text on a saved surface"""
        pygame.event.pump()
        if not(self._isheader):
            # load the image of the textbox
            self._screen.blit(
                self._surface, (self._surface_left_offset, self._surface_top_offset))
            pygame.event.pump()
        else:
            # self._bg_color
            self._screen.fill(white, (0, self._surface_top_offset,
                                      self._surface_width, self._size_per_line * self._line_number * 1 + self._top_offset))
            pygame.event.pump()

        counter = 0
        tx_font = self._font
        tx_color = self._txcolor
        pygame.event.pump()
        for i in line_list:

            self._screen.blit(tx_font.render(i, True, tx_color, self._bg_color),
                              self.line_list_rect_stored[counter])
            pygame.event.pump()
            counter += 1
        pygame.event.pump()
        if not(self._isheader):
            pygame.display.flip()
        else:
            pygame.display.update((0, self._top_offset,
                                   self._surface_width, self._size_per_line * self._line_number))
        pygame.event.pump()


def draw_one_sector(screen, sec_rectange, list_length_vertical, list_length_horizontal, l, list_rect, square_length, FPS, im, headroom: int=0)->None:
    white = (255, 255, 255)
    black = (0, 0, 0)
    # clock1 = pygame.time.Clock()
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
    processed_text.append("You helped avoid " + str(round(ounces_recycled *
                                                          energy_conversion, 3)) + " ounces")
    processed_text.append(
        " of CO2e emissions!")
    processed_text.append("Food is the single largest part of waste!")
    processed_text.append("Keeping it out of landfills is important!")
    pygame.event.pump()
    return processed_text


def recycle_text_processing(ounces_recycled: int = 0):
    energy_conversion = 3.1526066
    processed_text = []
    processed_text.append("Thank you for recycling")
    processed_text.append("You just recycled " +
                          str(round(ounces_recycled, 3)) + " ounces")
    processed_text.append("You just helped avoid " +
                          str(round(ounces_recycled *
                                    energy_conversion, 3)) + " ounces")
    processed_text.append(" of CO2e emissions!")
    pygame.event.pump()
    return processed_text


def landfill_text_processing(ounces_recycled: int = 0):
    processed_text = []
    processed_text.append(
        "It’s important to separate items that can’t be")
    processed_text.append("composted or recycled.")
    processed_text.append("Thank you!")
    processed_text.append(
        "Keeping landfill waste in the landfill bins allows other")
    processed_text.append("waste to be truly composted and recycled!")
    processed_text.append(
        "Keeping landfill items out of compost and")
    processed_text.append("recycling is important. Thank you!")
    pygame.event.pump()
    return processed_text
