import os
import sys
import time
import random
import pygame
from pygame.locals import *


if __name__ == '__main__':
    # intialize important things here
    pygame.init()
    # full screen
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    clock1 = pygame.time.Clock()
    font = pygame.font.SysFont('Calibri', 25, True)
    start = time.time()  # start of timer for when to draw

    # dictate the width, length and number of squares
    # all units are in pixel for this section
    square_length = 25  # the length of each small square in the sector
    list_legnth = 16  # number of squares in each sector=list_length^2
    total_square_length = 430  # total length of each sector square
    x_offset = 450  # x offset of the sector of the screen
    y_offset = 450  # y offset of the sector of the screen

    # auxillary variables
    FPS = 40  # FPS when drawing
    Compost = "Thanks for recyling compost"
    landfill = "Thanks for recyling landfill"
    current_pos = 0  # current section of the screen to be changed
    things_happened = True  # event for scale
    l = 0  # index of the current image to be displayed

    # color to be used
    white = (255, 255, 255)
    black = (0, 0, 0)

    screen_update_interval = 5.0  # float of how many seconds before drawing new image

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
    text_rect = Rect(0, 0, total_square_length, total_square_length)

    # begin with a white color
    screen.fill(white)
    pygame.display.flip()
    pygame.event.pump()  # used for keeping the OS happy

    # TODO: Refactor the code below
    # the code below will cycle through screen sector as well
    # as loaded images and display them with a defined time interval
    # the images are displayed gradually in order to create transition effects
    # as well as alleviate the load on the pi CPU
    while True:
        if (time.time() - start) > screen_update_interval:
            start = time.time()
            if current_pos == 0:
                screen.fill((white), top_rect)
                current_pos += 1
                for (i, j) in zip(range(0, list_legnth), range(0, list_legnth)):
                    for(k, v) in zip(range(0, i + 1), range(0, j + 1)):
                        screen.blit(im[l], list_toprect[k * list_legnth + j], (k *
                                                                               square_length, j * square_length, square_length, square_length))
                        screen.blit(im[l], list_toprect[i * list_legnth + v], (i *
                                                                               square_length, v * square_length, square_length, square_length))
                        pygame.event.pump()
                        pygame.display.flip()

                    clock1.tick(FPS)

            elif current_pos == 1:
                current_pos += 1
                screen.fill((white), mid_rect)
                for (i, j) in zip(range(0, list_legnth), range(0, list_legnth)):
                    for(k, v) in zip(range(0, i + 1), range(0, j + 1)):
                        screen.blit(im[l], list_midrect[k * list_legnth + j], (k *
                                                                               square_length, j * square_length, square_length, square_length))
                        screen.blit(im[l], list_midrect[i * list_legnth + v], (i *
                                                                               square_length, v * square_length, square_length, square_length))
                        pygame.event.pump()
                        pygame.display.flip()

                    clock1.tick(FPS)

            elif current_pos == 2:
                current_pos += 1
                screen.fill((white), bot_rect)
                for (i, j) in zip(range(0, list_legnth), range(0, list_legnth)):
                    for(k, v) in zip(range(0, i + 1), range(0, j + 1)):
                        screen.blit(im[l], list_botrect[k * list_legnth + j], (k *
                                                                               square_length, j * square_length, square_length, square_length))
                        screen.blit(im[l], list_botrect[i * list_legnth + v], (i *
                                                                               square_length, v * square_length, square_length, square_length))
                        pygame.event.pump()
                        pygame.display.flip()

                    clock1.tick(FPS)

            elif current_pos == 3:
                current_pos = 0
                screen.fill((white), botrigt_rect)
                for (i, j) in zip(range(0, list_legnth), range(0, list_legnth)):
                    for(k, v) in zip(range(0, i + 1), range(0, j + 1)):
                        screen.blit(im[l], list_botrightrect[k * list_legnth + j], (k *
                                                                                    square_length, j * square_length, square_length, square_length))
                        screen.blit(im[l], list_botrightrect[i * list_legnth + v], (i *
                                                                                    square_length, v * square_length, square_length, square_length))
                        pygame.event.pump()
                        pygame.display.flip()

                    clock1.tick(FPS)
            l = l + 1 if l < 8 else 0
        pygame.event.pump()
