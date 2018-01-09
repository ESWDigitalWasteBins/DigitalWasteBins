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
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock1 = pygame.time.Clock()
    font = pygame.font.Font(
        './test_new_format/Font_Folder/SourceSansPro-Black.ttf', 50)
    dist_btw_line = font.get_linesize()
    size_per_line = font.get_linesize()
    start = time.time()  # start of timer for when to draw

    #----------------------------------------------------
    # dictate the width, length and number of squares
    # all units are in pixel for this section
    square_length = 30  # the length of each small square in the sector

    # number of squares in each sector=list_length_vertical *list_length_horizontal
    list_length_vertical = 13
    list_length_horizontal = 60

    # total length of each sector square, used for allocating blank surface to draw on, usually allocate with a little headroom
    total_square_length = square_length * list_length_vertical
    x_offset = 0  # x offset of the sector of the screen
    y_offset_top = size_per_line  # y offset of the sector of the screen
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
    screen_update_interval = 3.0  # float of how many seconds before drawing new image

    #----------------------------------------------------
    # Used for loading images to be used into multiple squares
    im = []
    list_toprect = []
    list_midrect = []
    list_botrect = []

    # load images given by Tyson
    # TODO: Refactor the loading sections

    #----------------------------------------------------
    # used for selecting which mode to be in
    m = 'l'  # l for landfill, r for recycle and c for compost
    # set mode of running
    surface_left_offset = 70
    surface_top_offset = 0
    top_header_text = []
    bot_header_text = []
    if m == 'l':
        text_box_im = pygame.image.load((os.path.join(
            'test_new_format', 'bl' + '.png')))
        text_box_im.convert()
        total_line = 8
        top_header_text.append("                            LANDFILL/TRASH")
        bot_header_text.append("                                DL")
        header_offset = -400
        # surface_left_offset = 20
        # surface_top_offset = 20
        total_image = 9
        additional_left_offset = 300
        additiona_top_offset = 30
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
        additional_left_offset = 500
        additiona_top_offset = 120
        # surface_left_offset = 20
        # surface_top_offset = 20
        total_image = 9
    elif m == 'r':
        header_offset = -350
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
        # surface_left_offset = 20
        # surface_top_offset = 20

    for i in range(0, total_image):
        im.append(pygame.image.load(os.path.join(
            'test_new_format', m + str(i) + '.png')))
        im[i].convert()

    # Divide each section of the screen into many small squares to
    # draw gradually instead at once

    top_rect_offset_im = []
    mid_rect_offset_im = []
    # bot_rect_offset_im = []
    for k in im:
        for i in range(0, list_length_horizontal):
            for j in range(0, list_length_vertical):
                list_toprect.append(Rect(i * square_length + (screen.get_width() - k.get_width()) // 2, j *
                                         square_length + y_offset_top + 30, square_length, square_length))
        top_rect_offset_im.append(list_toprect)

        for i in range(0, list_length_horizontal):
            for j in range(0, list_length_vertical):
                list_midrect.append(Rect(i * square_length + (screen.get_width() - k.get_width()) // 2, total_square_length + j *
                                         square_length + y_offset_bot - 20, square_length, square_length))
        mid_rect_offset_im.append(list_midrect)

        # for i in range(0, list_length_horizontal):
        #     for j in range(0, list_length_vertical):
        #         list_botrect.append(Rect(i * square_length + (screen.get_width() - k.get_width()) // 2, j *
        #                                  square_length + 2 * total_square_length + y_offset, square_length, square_length))
        # bot_rect_offset_im.append(list_botrect)
        list_toprect = []
        list_midrect = []
        # list_botrect = []

    # rectange used for deleting before redraw of sections
    top_rect = Rect(0, y_offset_top + 30, screen.get_width(),
                    total_square_length)
    mid_rect = Rect(0, y_offset_bot + total_square_length, screen.get_width(),
                    total_square_length)

    # textbox image
    text_box_class = text_surface(
        screen, text_box_im, total_line, surface_left_offset + additional_left_offset, surface_top_offset + additiona_top_offset, surface_left_offset, surface_top_offset, black, "")

    # Initializing Top and Bottom header
    char_size = 15
    # offset the texts relative to each other for symmetry
    compensation = (len(top_header_text[0]) -
                    len(bot_header_text[0])) * char_size / 4
    # offset the text off the center for symmetry

    top_header = text_surface(
        screen, screen, 1, screen.get_width() / 2 + header_offset, 0, 0, 0, white, "", black, True)

    # bot_header = text_surface(
    #     screen, screen, 1, header_offset + screen.get_width() / 2 + compensation, 400, white, "", black, True)

    # begin with a white color
    screen.fill(white)
    pygame.event.pump()  # used for keeping the OS happy

    # testing = True
    # TODO: Refactor the code below
    # the code below will cycle through screen sector as well
    # as loaded images and display them with a defined time interval
    # the images are displayed gradually in order to create transition effects
    # as well as alleviate the load on the pi CPU

    # display initial image first
    # bot_header.draw_text_surface(bot_header_text)
    top_header.draw_text_surface(top_header_text)
    # weight = 5  # only for testing
    while (not(exited)):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE):
                    exited = True

        # if l%3==0:
        #     text_box_class.draw_text_surface(compost_text_processing(5))
        #     pygame.display.flip()

        if my_scale.ser.in_waiting > 0:
            reading = my_scale.ser.read(6)
            # unit are in ounces
            weight = my_scale.check(reading)
            if (weight):
                # unit is ounces of carbon emission
                screen.fill(white)
                # text_box_class.draw_text_surface(
                #     recycle_text_processing(weight))
                # text_box_class.draw_text_surface(
                #     compost_text_processing(weight))
                text_box_class.draw_text_surface(
                    landfill_text_processing(weight))
                pygame.display.flip()
                time.sleep(8)
                screen.fill(white)
        #         # bot_header.draw_text_surface(bot_header_text)
                top_header.draw_text_surface(top_header_text)
                pygame.display.flip()
        #         l = 3  # set so that images don't repeat immediately

        if (time.time() - start) > screen_update_interval:
            start = time.time()
            if current_pos == 0:
                current_pos += 1
                draw_one_sector(screen, top_rect, list_length_vertical, list_length_horizontal,
                                l, top_rect_offset_im[l], square_length, FPS, im)
            elif current_pos == 1:
                current_pos = 0
                draw_one_sector(screen, mid_rect, list_length_vertical, list_length_horizontal,
                                l, mid_rect_offset_im[l], square_length, FPS, im)

            l = l + 1 if l < total_image - 1 else 0
    pygame.quit()
    my_scale.ser.close()
