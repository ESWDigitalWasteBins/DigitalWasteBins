# ESW Digital Waste Bins

Watch the video that started it all!

[![University of Washington: Digital Bins - An Animated Waste Installation](https://img.youtube.com/vi/Ps0bFDG5O0c/0.jpg)](https://www.youtube.com/watch?v=Ps0bFDG5O0c)

## Development

We are developing the Digital Waste Bins software using Python 3 and the Pygame
library.

[Install Python 3 (scroll to the bottom of the page)](https://www.python.org/downloads/release/python-361/)

[Install Pygame](http://www.pygame.org/download.shtml)

## Testing

To run the project, open the command line (cmd on Windows, Terminal on Mac),
navigate to this directory, and run:

```
python3 -m dwb
```

Press the Escape key to exit.

## Requirements

A Python project that links each bin to a screen showing:

- Landfill
- Compost
- Recycle

Active:

- Compost: show possible things to put in that bin, cycles through it every 3-5 seconds
- Recycle: cups/cans
- Landfill: straws/wrappers
- Show diagram of what goes into which bin? (Starbucks cup: straw goes in landfill, cup goes into compost, etc.)

Interactive:

- Display Co<sub>2</sub> equivalent emissions: Thanks for throwing out \__ oz of \__.
- IDEAL: scan what is being thrown in and if it's correct
