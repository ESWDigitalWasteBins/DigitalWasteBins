
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
    # screen.fill((white))

    # screen.blit(text_box, text_rect)
    # pygame.display.flip()
    # screen.blit(font.render(Compost, True, (black)), text_rect)
    # pygame.display.flip()
    # time.sleep(1)
    # pygame.mouse.set_visible(0)

    # if things_happened:
    #     screen.fill((white))
    #     screen.blit(font.render(str(l), True, (black)), text_rect)
    #     time.sleep(1)
    #     screen.fill((white), text_rect)
    # if event.type == pygame.QUIT:
    #     break
    #     # Handle drawing
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
