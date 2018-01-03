import pygame
from pygame.locals import *

# contain the functions to draw each sector
# of the screen


def draw_one_sector(screen, sec_rectange, list_legnth, l, list_rect, square_length, FPS, im):
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
