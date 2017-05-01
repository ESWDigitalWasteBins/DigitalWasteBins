"""
scroll.py

Description:

Created Apr 29, 2017
"""


import pygame
from pathlib import Path


def main():
    pygame.init()

    # screen to draw on
    screen = pygame.display.set_mode((506, 900))
    width, height = screen.get_size()

    # test text
    text = pygame.font.Font(None, 100).render('Test', True, (0, 0, 0))
    twidth, theight = text.get_size()

    # physics
    speed_0_y = speed_y = 0  # initial speed and current speed
    accel_y = 0.3            # acceleration of falling images
    stop_y = 100             # stop y position for images
    wait_time = 1            # in seconds

    # framerate clock
    clock = pygame.time.Clock()

    # track cycling of frames
    running = True  # True if frames are cycling
    waited = False  # True if the frame has waited for wait_time seconds

    # image selection and location settings
    image_paths = list(Path('images/').glob('**/*.png'))  # get all PNG images from directory
    last_index = None  # index of the previous image
    curr_index = 0     # index of the current index

    # FIXME: first image, remove duplicate code
    image = pygame.image.load(str(image_paths[curr_index])).convert()
    iwidth, iheight = image.get_size()  # image dimensions
    scale = width/iwidth  # scale factor by width (for now, will change)
    image = pygame.transform.scale(image, (int(scale*iwidth), int(scale*iheight)))
    iwidth, iheight = image.get_size()  # image dimensions after scaling
    y_0 = y = -(theight + iheight)

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
        # Image details change when index changes,
        # so image updates only once per given frame
        # TODO: caching?
        if last_index is not None and last_index != curr_index:
            print('UPDATE @', y, 'last:', last_index, 'curr:', curr_index)
            last_index = curr_index  # update last index
            image = pygame.image.load(str(image_paths[curr_index])).convert()
            iwidth, iheight = image.get_size()  # image dimensions
            scale = width/iwidth  # scale by width
            image = pygame.transform.scale(image, (int(scale*iwidth), int(scale*iheight)))
            iwidth, iheight = image.get_size()  # image dimensions after scaling
            y_0 = y = -(theight + iheight)
        # Draw onto screen at y position
        screen.fill((255, 255, 255))
        screen.blit(text, (0, y))
        screen.blit(image, (0, y+theight))
        # Update y position
        if y >= height:
            print('NEXT @', y)
            y = y_0  # move image back to top
            screen.fill((255, 255, 255))  # white background
            waited = False  # after pausing for specified time
            # cycle through image indexes
            last_index, curr_index = curr_index, (curr_index + 1) % len(image_paths)
        else:
            speed_y += accel_y  # accelerate image
            y += speed_y  # change image position by speed amount
        # Update screen
        pygame.display.flip()
        # Pause once per cycle
        if not waited and y >= stop_y:
            print('STOP @', y)
            waited = True
            # FIXME: make y position static instead of pausing execution
            pygame.time.wait(wait_time * 1000)  # pause execution
            speed_y = speed_0_y  # reset speed to initial speed
        # 60 FPS
        clock.tick(60)


if __name__ == '__main__':
    main()
