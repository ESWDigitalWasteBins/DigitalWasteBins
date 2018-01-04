import pygame
from pygame.locals import *

# contain the functions to draw each sector
# of the screen


class text_surface:
    def __init__(self, screen, surface_image: pygame.surface, line_number: int=4, left_offset: int=0, top_offset: int=0,  color: (int, int, int)=(0, 0, 0), type_font: str="",  bg_color=(255, 255, 255)):
        self._bg_color = bg_color
        self._font = pygame.font.SysFont('Calibri', 70, True)
        self._height = self._font.get_height()
        self._size_per_line = (self._font).get_linesize()
        (self._surface_width, a) = surface_image.get_size()
        self._screen = screen
        self._surface = surface_image
        self._color = color
        # self._line_number = line_number

        self.line_list_rect_stored = []
        for counter in range(0, line_number):
            (self.line_list_rect_stored).append(pygame.Rect(
                left_offset, top_offset + counter * (self._size_per_line), self._surface_width, self._height))

    def draw_text_surface(self, line_list: [], header_rect=None) ->None:
        """draw text on a saved surface"""
        if header_rect == None:
            self._screen.fill(self._bg_color)
            self._screen.blit(self._surface, (0, 0))
        else:
            self._screen.fill((255, 255, 255))
            self._screen.fill(self._bg_color, header_rect)
        counter = 0
        tx_font = self._font
        tx_color = self._color
        for i in line_list:
            # self._screen.fill(self._bg_color, self.line_list_rect_stored[counter])
            self._screen.blit(tx_font.render(i, True, tx_color),
                              self.line_list_rect_stored[counter])
            counter += 1
        pygame.display.flip()


# def draw_header(self, screen, header_width, header_height,line_list, line_number: int=1, left_offset: int=0, top_offset: int=0, color: (int, int, int)=(0, 0, 0), type_font: str="",top=True)->None:
#     if top:
#         screen.blit((0,0,header_width, header_height),(0,0))
#     else:
#         screen.blit((0,0,header_width, header_height),(0,screen.get_height-header_height))
#     type_font=pygame.font.SysFont('Calibri', 70, True)

#     for i in line_list:
#         screen.blit(type_font.render(i, True, color), Rect())

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
                                                         energy_conversion) + " ounces")
    processed_text.append(" of carbone-equivalent emissions!")
    processed_text.append(
        "Food waste is the single largest part of waste.")
    processed_text.append("Keeping it out of landfills is important!")
    return processed_text


def recycle_text_processing(ounces_recycled: int = 0):
    energy_conversion = 3.1526066
    processed_text = []
    processed_text.append("Thank you for recycling")
    processed_text.append("You just composted " +
                          str(ounces_recycled) + " ounces")
    processed_text.append("You just helped avoid " +
                          str(ounces_recycled * energy_conversion) + " ounces")


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
