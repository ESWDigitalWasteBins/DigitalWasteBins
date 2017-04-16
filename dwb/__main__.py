import pygame


def start():

    # Initialize a fullscreen window
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Window title
    pygame.display.set_caption('ESW Digital Waste Bins')

    # Game loop
    clock = pygame.time.Clock()
    running = True
    while running:

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

        # Next frame (20 fps)
        clock.tick(20)

        # Repaint screen
        pygame.display.flip()

    # Exit
    pygame.quit()


start()
