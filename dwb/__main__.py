"""
__main__.py

Description: Run this for digital waste bins.

Created on Apr 15, 2017
"""


import pygame
from scale import scaleReading
from motionSensor import motionReading
from font_manager import FontManager
from display import Title, Content, Display


WHITE = (255, 255, 255)
BLUE = (0, 57, 166)
GREEN = (24, 165, 75)
BLACK = (7, 16, 19)


# 0.5 is arbitary number that will be changed
MIN_WEIGHT_DIFF = 0.5


def main() -> None:
    mode = input('MODE (L, R, C): ')

    # Initialize a fullscreen window
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    # Window title
    pygame.display.set_caption('ESW Digital Waste Bins')

    # Make a display
    # TODO: add more modules to the display
    # TODO: store in subclass? for each bin
    # Landfill
    if mode == 'L':
        title_fm = FontManager(['impact'])
        text = title_fm.create_text('LANDFILL', 100, color=WHITE)
        title = Title(text=text, bg=BLACK, pady=100)
        content = Content(display_bg_color=WHITE)
        Display(title, content).draw(screen)
    # Compost
    elif mode == 'C':
        title_fm = FontManager(['impact'])
        text = title_fm.create_text('COMPOST', 100, color=WHITE)
        title = Title(text=text, bg=GREEN, pady=100)
        content = Content(display_bg_color=WHITE)
        Display(title, content).draw(screen)
    # Recycle
    elif mode == 'R':
        title_fm = FontManager(['impact'])
        text = title_fm.create_text('RECYCLE', 100, color=WHITE)
        title = Title(text=text, bg=BLUE, pady=100)
        content = Content(display_bg_color=WHITE)
        Display(title, content).draw(screen)
    else:
        print('Not a valid option.')
        return None

    # Game loop
    clock = pygame.time.Clock()
    running = True
    prev_reading = scaleReading()  # initial scale reading

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
        curr_reading = scaleReading()
        weight_diff = curr_reading-prev_reading
        # check if the reading has changed compared to last time
        if weight_diff > MIN_WEIGHT_DIFF and motionReading():
            # start telling the thrower how much he she saved etc
            prev_reading = curr_reading
        elif weight_diff < MIN_WEIGHT_DIFF and motionReading():
            # thank the thrower but don't display the weight
            prev_reading = curr_reading
        else:
            prev_reading = curr_reading

        # Next frame (20 fps)
        clock.tick(20)

        # Repaint screen
        pygame.display.flip()
    # Exit
    pygame.quit()


if __name__ == '__main__':
    main()
