"""Mode represents a collection of data for a specific bin."""


from pathlib import Path


class Mode:
    """Mode"""

    def __init__(self, display_str: str, image_path: Path,
                 text_color: (int, int, int), bg_color: (int, int, int)):
        """Initialize Mode with attributes."""
        self.display_str = display_str
        self.image_path = image_path
        self.text_color = text_color
        self.bg_color = bg_color
