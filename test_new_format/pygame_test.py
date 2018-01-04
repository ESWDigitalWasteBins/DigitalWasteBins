import os
import sys
import time
import random
import pygame
from pygame.locals import *
from sector_draw import *
#from scale import Scale
from collections import namedtuple

if __name__ == '__main__':
    #----------------------------------------------------
    # intialize important things here
    pygame.init()
    #my_scale = Scale()
    # full screen
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock1 = pygame.time.Clock()
    font = pygame.font.SysFont('Calibri', 70, True)
    start = time.time()  # start of timer for when to draw

    #----------------------------------------------------
    # dictate the width, length and number of squares
    # all units are in pixel for this section
    square_length = 25  # the length of each small square in the sector
    list_legnth = 16  # number of squares in each sector=list_length^2
    head_room = 20
    # total length of each sector square, used for allocating blank surface to draw on, usually allocate with a little headroom
    total_square_length = square_length * list_legnth + head_room
    x_offset = 450  # x offset of the sector of the screen
    y_offset = 450  # y offset of the sector of the screen
    top_header_width = screen.get_width()
    top_header_height = 500
    bot_header_width = screen.get_width()
    bot_header_height = 500

    #----------------------------------------------------
    # auxillary variables
    FPS = 0  # FPS when drawing
    current_pos = 0  # current section of the screen to be changed
    things_happened = True  # event for scale
    l = 0  # index of the current image to be displayed
    exited = False  # indicate if user wants to exit
    # color to be used
    white = (255, 255, 255)
    black = (0, 0, 0)
    screen_update_interval = 1.0  # float of how many seconds before drawing new image

    #----------------------------------------------------
    # Used for loading images to be used into multiple squares
    im = []
    list_toprect = []
    list_midrect = []
    list_botrect = []
    list_botrightrect = []

    # load images given by Tyson
    # TODO: Refactor the loading sections

    # Divide each section of the screen into many small squares to
    # draw gradually instead at once
    for i in range(0, list_legnth):
        for j in range(0, list_legnth):
            list_toprect.append(Rect(i * square_length, j *
                                     square_length, square_length, square_length))

    for i in range(0, list_legnth):
        for j in range(0, list_legnth):
            list_midrect.append(Rect(i * square_length, y_offset + j *
                                     square_length, square_length, square_length))

    for i in range(0, list_legnth):
        for j in range(0, list_legnth):
            list_botrect.append(Rect(i * square_length, 2 * y_offset + j *
                                     square_length, square_length, square_length))

    # for i in range(0, list_legnth):
    #     for j in range(0, list_legnth):
    #         list_botrightrect.append(Rect(i * square_length + x_offset,  j *
    #                                       square_length + y_offset, square_length, square_length))

    # rectange used for deleting before redraw of sections
    top_rect = Rect(x_offset, 0, total_square_length, total_square_length)
    mid_rect = Rect(x_offset, y_offset, total_square_length,
                    total_square_length)
    bot_rect = Rect(x_offset, y_offset * 2,
                    total_square_length, total_square_length)

    # botrigt_rect = Rect(x_offset, y_offset,
    #                    total_square_length, total_square_length)
    top_header_rect = Rect(0, 0, top_header_width, top_header_height)
    bot_header_rect = Rect(
        screen.get_height() - bot_header_height, 0, bot_header_width, bot_header_height)
    #----------------------------------------------------
    # used for selecting which mode to be in
    m = 'c'  # l for landfill, r for recycle and c for compost
    # set mode of running
    top_header_text = []
    bot_header_text = []
    if m == 'l':
        text_box_im = pygame.image.load((os.path.join(
            'test_new_format', 'bl' + '.png')))
        text_box_im.convert()
        total_line = 6
        top_header_text.append("Food Scraps")
        bot_header_text.append("Landfill")
    elif m == 'c':
        text_box_im = pygame.image.load((os.path.join(
            'test_new_format', 'gt' + '.png')))
        text_box_im.convert()
        total_line = 6
        top_header_text.append("Soiled Containers")
        bot_header_text.append("Compost")
    elif m == 'r':
        text_box_im = pygame.image.load((os.path.join(
            'test_new_format', 'bt' + '.png')))
        text_box_im.convert()
        total_line = 4
        top_header_text.append("Non-soiled Containers")
        bot_header_text.append("recycle")

    for i in range(0, 9):
        im.append(pygame.image.load(os.path.join(
            'test_new_format', m + str(i) + '.png')))
        im[i].convert()

    text_box_class = text_surface(
        screen, text_box_im, total_line, 130, 150, black, "")

    top_header = text_surface(screen, screen, 2, 0, 0, white, "", black)
    top_header.draw_text_surface(top_header_text, top_header_rect)

    bot_header = text_surface(
        screen, screen, 2, 0, screen.get_height() - bot_header_height, white, "", black)
    bot_header.draw_text_surface(bot_header_text, bot_header_rect)
    time.sleep(5)
    # begin with a white color
    screen.fill(white)
    pygame.display.flip()
    pygame.event.pump()  # used for keeping the OS happy

    testing = True
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

        # if testing and l % 3 == 0:
        #     text_box_class.draw_text_surface(compost_text_processing(5))
        #     time.sleep(5)
        #     screen.fill(white)

        # if my_scale.ser.in_waiting > 0:
        #     reading = my_scale.ser.read(6)
        #     # unit are in ounces
        #     weight = my_scale.check(reading)
        #     if (weight):
        #         energy_saved = weight * energy_conversion  # unit is ounces of carbon emission
        #         screen.fill((white))
        #         screen.blit(font.render(compost, True, (black)), text_rect)
        #         screen.blit(font.render(
        #             str(energy_saved), True, (black)), weight_rect)
        #         pygame.display.flip()
        #         time.sleep(3)
        #         screen.fill((white))
        #         pygame.display.flip()
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
                current_pos = 0
                draw_one_sector(screen, bot_rect, list_legnth,
                                l, list_botrect, square_length, FPS, im)

            # elif current_pos == 3:
            #     current_pos = 0
            #     draw_one_sector(screen, botrigt_rect, list_legnth,
            #                     l, list_botrightrect, square_length, FPS, im)

            l = l + 1 if l < 8 else 0
        # pygame.event.pump()
    pygame.quit()
    # my_scale.ser.close()
