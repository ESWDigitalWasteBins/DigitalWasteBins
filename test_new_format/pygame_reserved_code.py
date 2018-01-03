
# Used for random rendering
list_i = random.sample(range(0, list_legnth), list_legnth)
    list_j = random.sample(range(0, list_legnth), list_legnth)
    screen.fill((white))
    for i in list_i:
        for j in list_j:
            screen.blit(im[0], list_rect[i * list_legnth + j], (i *
                                                                square_length, j * square_length, square_length, square_length))

# Used for diagonal rendering
clock1 = pygame.time.Clock()
for (i, j) in zip(range(0, list_legnth), range(0, list_legnth)):
    for(k, v) in zip(range(0, i + 1), range(0, j + 1)):
        screen.blit(im[0], list_rect[k * list_legnth + j], (k *
                                                            square_length, j * square_length, square_length, square_length))
        screen.blit(im[0], list_rect[i * list_legnth + v], (i *
                                                            square_length, v * square_length, square_length, square_length))
        pygame.display.flip()
    clock1.tick(50)
