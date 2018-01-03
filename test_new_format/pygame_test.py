import os
import sys
import time
import random
import pygame
from pygame.locals import *
square_length = 25
list_legnth = 16  # used to be 650 pixel
total_square_length = 430
pygame.init()
im = []
list_toprect = []
list_midrect = []
list_botrect = []
list_botrightrect = []

x_offset = 450
y_offset = 450
FPS = 30
picture_update_frequency = 1.0 / 60
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
for i in range(0, 9):
    im.append(pygame.image.load('c' + str(i) + '.png'))
    im[i].convert()
text_box = pygame.image.load('burger.png')
text_box.convert()
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
        list_botrect.append(Rect(i * square_length + x_offset,  j *
                                 square_length, square_length, square_length))

for i in range(0, list_legnth):
    for j in range(0, list_legnth):
        list_botrightrect.append(Rect(i * square_length + x_offset,  j *
                                      square_length + y_offset, square_length, square_length))

clock1 = pygame.time.Clock()
clock2 = pygame.time.Clock()
white = (255, 255, 255)
black = (0, 0, 0)
Compost = "Thanks for recyling compost"
landfill = "Thanks for recyling landfill"
start = time.time()
if __name__ == '__main__':
    font = pygame.font.SysFont('Calibri', 25, True)

    # screen.blit(font.render(landfill,
    #                        True, (white)), (380, 860))
    top_rect = Rect(0, 0, total_square_length, total_square_length)
    mid_rect = Rect(0, y_offset, total_square_length, total_square_length)
    bot_rect = Rect(x_offset, 0, total_square_length, total_square_length)
    botrigt_rect = Rect(x_offset, y_offset,
                        total_square_length, total_square_length)
    text_rect = Rect(0, 0, total_square_length, total_square_length)
    # k = 0
    screen.fill(white)
    pygame.display.flip()
    current_pos = 0
    things_happened = True
    l = 0
    # for event in pygame.event.get():
    while True:

        # if things_happened:
        #     screen.fill((white))
        #     screen.blit(font.render(str(l), True, (black)), text_rect)
        #     time.sleep(1)
        #     screen.fill((white), text_rect)
        # if event.type == pygame.QUIT:
        #     break
        #     # Handle drawing

        if (time.time() - start) > 0.5:
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
            # divide into two half and pump in between to make sure that the system doesn't forget pygame is running
            l = l + 1 if l < 8 else 0
        pygame.event.pump()
        # l += 1
    # screen.fill((white))

    # screen.blit(text_box, text_rect)
    # pygame.display.flip()
    # screen.blit(font.render(Compost, True, (black)), text_rect)
    # pygame.display.flip()
    # time.sleep(1)
    # pygame.mouse.set_visible(0)
