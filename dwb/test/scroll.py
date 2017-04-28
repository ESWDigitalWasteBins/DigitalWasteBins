import pygame


def main():
    pygame.init()

    screen = pygame.display.set_mode((500, 500), pygame.DOUBLEBUF | pygame.HWSURFACE)
    width, height = screen.get_size()

    text = pygame.font.Font(None, 100).render('Test', True, (255, 255, 255))
    twidth, theight = text.get_size()

    image = pygame.image.load('test.png')
    iwidth, iheight = image.get_size()
    scale = width/iwidth  # scale by width
    image = pygame.transform.scale(image, (int(scale*iwidth), int(scale*iheight)))

    y_0 = y = -(theight + iheight)

    speed_0_y = speed_y = 0  # initial speed and current speed
    accel_y = 0.3  # acceleration of falling images
    stop_y = 100  # stop y position for images
    wait_time = 5  # seconds

    clock = pygame.time.Clock()

    running = True
    waited = False

    while running:
        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
        # Draw onto screen
        screen.fill(0)
        screen.blit(text, (0, y))
        screen.blit(image, (0, y))
        # Update y position
        if y >= height:
            y = y_0  # reset y position to starting position
            waited = False
        else:
            speed_y += accel_y
            y += speed_y
        # Update screen
        pygame.display.flip()
        # Pause once per cycle
        if not waited and y >= stop_y:
            print(y)
            waited = True
            pygame.time.wait(wait_time * 1000)
            speed_y = speed_0_y  # reset speed to initial speed
        # 60 FPS
        clock.tick(60)


if __name__ == '__main__':
    main()
