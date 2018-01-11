import os
import sys
import time
import random
import pygame
from pygame.locals import *
from sector_draw import *
from scale import Scale
from collections import namedtuple

if __name__ == '__main__':
    #----------------------------------------------------
    # intialize important things here
    pygame.init()
    my_scale = Scale()
    # full screen
    screen = pygame.display.set_mode(
        (0, 0), pygame.FULLSCREEN)
    clock1 = pygame.time.Clock()
    font = pygame.font.Font(
        './test_new_format/Font_Folder/SourceSansPro-Black.ttf', 50)
    dist_btw_line = font.get_linesize()
    size_per_line = font.get_linesize()
    start = time.time()  # start of timer for when to draw

    #----------------------------------------------------
    # dictate the width, length and number of squares
    # all units are in pixel for this section
    square_length = 20  # the length of each small square in the sector

    # number of squares in each sector=list_length_vertical *list_length_horizontal
    list_length_vertical = 14
    list_length_horizontal = 85

    # total length of each sector square, used for allocating blank surface to draw on, usually allocate with a little headroom
    total_square_vertical_length = square_length * list_length_vertical
    total_square_horizontal_length = square_length * list_length_horizontal
    x_offset = 0  # x offset of the sector of the screen
    y_offset_top = 2 * size_per_line  # y offset of the sector of the screen
    y_offset_bot = 200
    top_header_width = screen.get_width()
    top_header_height = 200
    bot_header_width = screen.get_width()
    bot_header_height = 200

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
    blue = (42, 106, 255)
    green = (23, 219, 36)
    screen_update_interval = 3.0  # float of how many seconds before drawing new image

    #----------------------------------------------------
    # Used for loading images to be used into multiple squares
    im = []
    list_toprect = []
    list_midrect = []
    list_botrect = []

    # load images given by Tyson
    # TODO: Refactor the loading sections
    pygame.event.pump()
    #----------------------------------------------------
    # used for selecting which mode to be in
    m = 'r'  # l for landfill, r for recycle and c for compost
    # set mode of running
    surface_left_offset = 70
    surface_top_offset = 0
    top_header_text = []
    bot_header_text = []
    if m == 'l':
        text_box_im = pygame.image.load((os.path.join(
            'test_new_format', 'bl' + '.png')))
        text_box_im.convert()
        total_line = 7
        top_header_text.append("                            LANDFILL")
        bot_header_text.append("                                DL")
        header_offset = -400
        # surface_left_offset = 20
        # surface_top_offset = 20
        total_image = 9
        additional_left_offset = 300
        additiona_top_offset = 30
        background_color = black
        # surface_left_offset -= 30
    elif m == 'c':
        text_box_im = pygame.image.load((os.path.join(
            'test_new_format', 'gt' + '.png')))
        text_box_im.convert()
        total_line = 6
        top_header_text.append(
            "               COMPOST")
        bot_header_text.append(
            "Compost")
        header_offset = -200
        additional_left_offset = 450
        additiona_top_offset = 90
        background_color = green
        # surface_left_offset = 20
        # surface_top_offset = 20
        total_image = 9
    elif m == 'r':
        header_offset = -530
        text_box_im = pygame.image.load((os.path.join(
            'test_new_format', 'bt' + '.png')))
        text_box_im.convert()
        total_line = 5
        total_image = 5
        top_header_text.append(
            "                            RECYCLE")
        bot_header_text.append("                                Recycle")
        additional_left_offset = 500
        additiona_top_offset = 120
        background_color = blue
        # surface_left_offset = 20
        # surface_top_offset = 20
    pygame.event.pump()
    for i in range(0, total_image):
        im.append(pygame.image.load(os.path.join(
            'test_new_format', m + str(i) + '.png')))
        im[i].convert()

    # Divide each section of the screen into many small squares to
    # draw gradually instead at once
    pygame.event.pump()
    screen.fill(white)
    pygame.display.flip()
    toprect_offset_im = []
    midrect_offset_im = []
    botrect_offset_im = []
    for k in im:
        toprect = Rect((screen.get_width() - k.get_width()) //
                       2, y_offset_top, total_square_horizontal_length, total_square_vertical_length)
        midrect = Rect((screen.get_width() - k.get_width()) //
                       2, y_offset_top + total_square_vertical_length, total_square_horizontal_length, total_square_vertical_length)
        botrect = Rect((screen.get_width() - k.get_width()) //
                       2, y_offset_top + 2 * total_square_vertical_length, total_square_horizontal_length, total_square_vertical_length)
        toprect_offset_im.append(toprect)
        midrect_offset_im.append(midrect)
        botrect_offset_im.append(botrect)
        pygame.event.pump()

    # rectange used for deleting before redraw of sections
    section_num = 3
    top_rect = Rect(0, y_offset_top, screen.get_width(),
                    total_square_vertical_length)
    mid_rect = Rect(0, y_offset_top + total_square_vertical_length, screen.get_width(),
                    total_square_vertical_length)
    bot_rect = Rect(0, y_offset_top + 2 * total_square_vertical_length, screen.get_width(),
                    total_square_vertical_length)

    # textbox image
    text_box_class = text_surface(
        screen, text_box_im, total_line, surface_left_offset + additional_left_offset, surface_top_offset + additiona_top_offset, surface_left_offset, surface_top_offset, black, "")

    # Initializing Top and Bottom header

    top_header = text_surface(
        screen, screen, 1, screen.get_width() / 2 + header_offset, 0.25 * dist_btw_line, 0, 0, white, "", background_color, True)

    # begin with a white color
    screen.fill(white)
    pygame.event.pump()  # used for keeping the OS happy

    # draw header first
    top_header.draw_text_surface(top_header_text)
    # weight = 5  # only for testing
    while (not(exited)):
        # pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE):
                    exited = True

        # if l%3==0:
        #     text_box_class.draw_text_surface(compost_text_processing(5))
        #     pygame.display.flip()

        if my_scale.ser.in_waiting >= 6:

            # check if the scale is responding correctly
            reading = my_scale.ser.read(6)
            while (len(reading) != 6 or reading[0] != 0xff):
                my_scale.ser.close()
                my_scale.ser.open()
                reading = my_scale.ser.read(6)

                # wait for it to get real data
                # unit are in ounces
            if not(reading[2] == my_scale.raw[2] and reading[3] == my_scale.raw[3] and reading[1] == my_scale.raw[1] and reading[4] == my_scale.raw[4]):
                weight = my_scale.check(reading)
                if (weight):
                    screen.fill(white)
                    text_box_class.draw_text_surface(
                        recycle_text_processing(weight))
                    pygame.display.flip()
                    pygame.event.pump()
                    time.sleep(8)
                    screen.fill(white)
                    top_header.draw_text_surface(top_header_text)
                    pygame.event.pump()
                    pygame.display.flip()

        if (time.time() - start) > screen_update_interval:
            start = time.time()
            if current_pos == 0:
                current_pos = +1
                pygame.event.pump()
                screen.fill((white), top_rect)
                screen.blit(im[l], toprect_offset_im[l])
                pygame.display.update(top_rect)
            elif current_pos == 1:
                current_pos += 1
                pygame.event.pump()
                screen.fill((white), mid_rect)
                screen.blit(im[l], midrect_offset_im[l])
                pygame.display.update(mid_rect)
            elif current_pos == 2:
                current_pos = 0
                pygame.event.pump()
                screen.fill((white), bot_rect)
                screen.blit(im[l], botrect_offset_im[l])
                pygame.display.update(bot_rect)
            l = l + 1 if l < total_image - 1 else 0
    pygame.quit()
    my_scale.ser.close()
