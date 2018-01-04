import os
import sys
import time
import random
import pygame
from pygame.locals import *
from sector_draw import *
from scale import Scale
from frame import Frame
from header import Header
from body import Body
from collections import namedtuple


if __name__ == '__main__':
    # intialize important things here
    pygame.init()
    my_scale = Scale()
    # full screen
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock1 = pygame.time.Clock()
    font = pygame.font.SysFont('Calibri', 70, True)
    start = time.time()  # start of timer for when to draw

    # dictate the width, length and number of squares
    # all units are in pixel for this section
    square_length = 25  # the length of each small square in the sector
    list_legnth = 16  # number of squares in each sector=list_length^2
    head_room = 20
    # total length of each sector square, used for allocating blank surface to draw on, usually allocate with a little headroom
    total_square_length = square_length * list_legnth + head_room
    x_offset = 450  # x offset of the sector of the screen
    y_offset = 450  # y offset of the sector of the screen
    header_width = 1000
    header_height = 500
    # auxillary variables
    FPS = 0  # FPS when drawing
    Compost = "Thanks for recyling compost"
    landfill = "Thanks for recyling landfill"
    current_pos = 0  # current section of the screen to be changed
    things_happened = True  # event for scale
    l = 0  # index of the current image to be displayed
    exited = False  # indicate if user wants to exit
    # color to be used
    white = (255, 255, 255)
    black = (0, 0, 0)

    screen_update_interval = 1.0  # float of how many seconds before drawing new image

    # Used for loading images to be used into multiple squares
    im = []
    list_toprect = []
    list_midrect = []
    list_botrect = []
    list_botrightrect = []

    # load images given by Tyson
    for i in range(0, 9):
        im.append(pygame.image.load(os.path.join(
            'test_new_format', 'c' + str(i) + '.png')))
        im[i].convert()
    for i in range(0, list_legnth):
        for j in range(0, list_legnth):
            list_toprect.append(Rect(i * square_length, j *
                                     square_length, square_length, square_length))

    # Divide each section of the screen into many small squares to
    # draw gradually instead at once
    for i in range(0, list_legnth):
        for j in range(0, list_legnth):
            list_midrect.append(Rect(i * square_length, y_offset + j *
                                     square_length, square_length, square_length))

    for i in range(0, list_legnth):
        for j in range(0, list_legnth):
            list_botrect.append(Rect(i * square_length + x_offset,  j *
                                     square_length, square_length, square_length))

    for i in range(0, list_legnth):
        for j in range(0, list_legnth):
            list_botrightrect.append(Rect(i * square_length + x_offset,  j *
                                          square_length + y_offset, square_length, square_length))

    # rectange used for deleting before redraw of sections
    top_rect = Rect(0, 0, total_square_length, total_square_length)
    mid_rect = Rect(0, y_offset, total_square_length, total_square_length)
    bot_rect = Rect(x_offset, 0, total_square_length, total_square_length)
    botrigt_rect = Rect(x_offset, y_offset,
                        total_square_length, total_square_length)
    text_rect = Rect(0, 0, header_width, header_height)
    weight_rect = Rect(0, 20, header_width, header_height)
    m = 'L'  # L for landfill, R for recycle and
    # set mode of running
    if m == 'L':
        energy_conversion = 1  # no specific conversion factor for landfill

    elif m == 'C':
        energy_conversion = 0.3968316

    elif m == 'R':
        energy_conversion = 3.1526066

    # begin with a white color
    screen.fill(white)
    pygame.display.flip()
    pygame.event.pump()  # used for keeping the OS happy

    # TODO: Refactor the code below
    # the code below will cycle through screen sector as well
    # as loaded images and display them with a defined time interval
    # the images are displayed gradually in order to create transition effects
    # as well as alleviate the load on the pi CPU
    while (not(exited)):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE):
                    exited = True

        if my_scale.ser.in_waiting > 0:
            reading = my_scale.ser.read(6)
            # unit are in ounces
            weight = my_scale.check(reading)
            if (weight):
                energy_saved = weight * energy_conversion  # unit is ounces of carbon emission
                screen.fill((white))
                screen.blit(font.render(Compost, True, (black)), text_rect)
                screen.blit(font.render(
                    str(weight), True, (black)), weight_rect)
                pygame.display.flip()
                time.sleep(3)
                screen.fill((white))
                # if weight != 0:
                # display.is_using_scale = Tru
                # elif display.frame_type == 1:
                # display.is_using_scale=False
        if (time.time() - start) > screen_update_interval:
            start = time.time()
            if current_pos == 0:
                current_pos += 1
                draw_one_sector(screen, top_rect, list_legnth,
                                l, list_toprect, square_length, FPS, im)
            elif current_pos == 1:
                current_pos += 1
                draw_one_sector(screen, mid_rect, list_legnth,
                                l, list_midrect, square_length, FPS, im)

            elif current_pos == 2:
                current_pos += 1
                draw_one_sector(screen, bot_rect, list_legnth,
                                l, list_botrect, square_length, FPS, im)

            elif current_pos == 3:
                current_pos = 0
                draw_one_sector(screen, botrigt_rect, list_legnth,
                                l, list_botrightrect, square_length, FPS, im)

            l = l + 1 if l < 8 else 0
        # pygame.event.pump()
    pygame.quit()
    my_scale.ser.close()
