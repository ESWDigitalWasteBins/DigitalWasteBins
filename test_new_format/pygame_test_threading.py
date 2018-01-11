import os
import sys
import time
import random
import pygame
from pygame.locals import *
from sector_draw import *
from collections import namedtuple
import threading
from scale_threading import Scale_Thread

if __name__ == '__main__':
    #----------------------------------------------------
    # intialize important things here
    pygame.init()
    # full screen
    screen = pygame.display.set_mode(
        (0, 0), pygame.FULLSCREEN)
    clock1 = pygame.time.Clock()
    font = pygame.font.Font(
        './test_new_format/Font_Folder/SourceSansPro-Black.ttf', 40)
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
    screen_update_interval = 5.0  # float of how many seconds before drawing new image

    #----------------------------------------------------
    # Used for loading images to be used into multiple squares
    im = []
    list_toprect = []
    list_midrect = []
    list_botrect = []

    # load images given by Tyson
    # TODO: Refactor the loading sections
    # pygame.event.pump()
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
        total_line = 7
        top_header_text.append("                            LANDFILL")
        bot_header_text.append("                                DL")
        header_offset = -575  # tested
        # surface_left_offset = 20
        # surface_top_offset = 20
        total_image = 9
        additional_left_offset = 300
        additiona_top_offset = 10
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
        header_offset = -350
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
    # pygame.event.pump()
    for i in range(0, total_image):
        im.append(pygame.image.load(os.path.join(
            'test_new_format', m + str(i) + '.png')))
        im[i].convert()

    # Divide each section of the screen into many small squares to
    # draw gradually instead at once
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
        # pygame.event.pump()

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
        screen, screen, 1, screen.get_width() / 2 + header_offset, 0, 0, 0, white, "", background_color, True)

    # begin with a white color

    # draw header first
    scale_lock = threading.RLock()
    scale_thread = Scale_Thread(
        screen, scale_lock, text_box_class, top_header, top_header_text, im,  toprect_offset_im,  midrect_offset_im, botrect_offset_im, top_rect, mid_rect, bot_rect)
    screen.fill(white)

    # display default image on startup
    top_header.draw_text_surface(top_header_text)
    screen.fill((white), top_rect)
    screen.fill((white), mid_rect)
    screen.fill((white), bot_rect)
    screen.blit(im[0], toprect_offset_im[0])
    screen.blit(im[1], midrect_offset_im[1])
    screen.blit(im[2], botrect_offset_im[2])
    l = 3
    pygame.display.flip()
    failed_acquire_count = 0
    scale_thread.start()
    # weight = 5  # only for testing
    while (not(exited)):
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE):
                    exited = True

        if (time.time() - start) > screen_update_interval:
            pygame.event.pump()
            while(not(scale_lock.acquire(blocking=False))):
                failed_acquire_count += 1
                pygame.event.pump()
            if failed_acquire_count != 0:
                l = l + 3 if l < total_image - 3 else 0
            failed_acquire_count = 0
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
            scale_lock.release()
            l = l + 1 if l < total_image - 1 else 0
    pygame.quit()
