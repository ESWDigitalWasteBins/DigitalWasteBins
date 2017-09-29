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
    screen = pygame.display.set_mode((400, 900))
    width, height = screen.get_size()

    # test text
    text = pygame.font.Font(None, 100).render('Test', True, (0, 0, 0))
    twidth, theight = text.get_size()

    # physics
    speed_0_y = speed_y = 0  # initial speed and current speed
    accel_y = 0.3            # acceleration of falling images
    wait_time = 1000            # in milliseconds

    # framerate clock
    clock = pygame.time.Clock()

    # track cycling of frames
    running = True  # True if frames are cycling
    waited = False  # True if the frame has waited for wait_time seconds
    waiting = False
    time_start = None  # start waiting
    time_now = pygame.time.get_ticks()

    # image selection and location settings
    image_paths = list(Path('images/').glob('**/*.png'))  # get all PNG images from directory
    last_index = None  # index of the previous image
    curr_index = 0     # index of the current index

    # FIXME: first image, remove duplicate code
    image = pygame.image.load(str(image_paths[curr_index])).convert()
    iwidth, iheight = image.get_size()    # image dimensions
    scale_y = (height-theight) / iheight  # scale by height
    scale_x = width / iwidth              # scale by width
    scale = min(scale_x, scale_y)
    if scale > 1:
        scale = 1
    image = pygame.transform.scale(image, (int(scale*iwidth), int(scale*iheight)))
    iwidth, iheight = image.get_size()  # image dimensions after scaling
    y_0 = y = -(theight + iheight)
    stop_y = (height - (theight + iheight)) // 2  # stop at center of screen

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
            iwidth, iheight = image.get_size()    # image dimensions
            scale_y = (height-theight) / iheight  # scale by height
            scale_x = width / iwidth              # scale by width
            scale = min(scale_x, scale_y)
            if scale > 1:
                scale = 1
            image = pygame.transform.scale(image, (int(scale*iwidth), int(scale*iheight)))
            iwidth, iheight = image.get_size()  # image dimensions after scaling
            y_0 = y = -(theight + iheight)
            stop_y = (height - (theight + iheight)) // 2
        # Draw onto screen at y position
        screen.fill((255, 255, 255))
        screen.blit(text, (0, y))
        screen.blit(image, (0, y+theight))
        # check if image has waited specified amount of time
        if not waited and not waiting and y >= stop_y:
            print('STOP @', y)
            time_start = pygame.time.get_ticks()
            waiting = True
        time_now = pygame.time.get_ticks()
        if waiting and time_start and time_now - time_start >= wait_time:
            waited = True
            waiting = False
            speed_y = speed_0_y  # reset speed to initial speed
        # Update y position only if not waiting
        if not waiting:
            if y >= height:
                print('NEXT @', y)
                # FIXME: Remove this possibly?
                y = y_0  # move image back to top
                waited = False  # after pausing for specified time
                # cycle through image indexes
                last_index, curr_index = curr_index, (curr_index + 1) % len(image_paths)
            else:
                speed_y += accel_y  # accelerate image
                y += speed_y  # change image position by speed amount
        # Update screen
        pygame.display.flip()
        # 60 FPS
        clock.tick(60)


if __name__ == '__main__':
    main()
