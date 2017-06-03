import pygame


pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE)

clock = pygame.time.Clock()
running = True

y = 0

rect = pygame.Rect(0, 0, 500, 500)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                break

    screen.fill((0, 0, 0))

    rect.center = (screen.get_width()//2, y)
    pygame.draw.rect(screen, (255, 255, 255), rect)

    y += 10

    if y >= screen.get_height():
        y = 0

    clock.tick(60)

    pygame.display.flip()

pygame.quit()
