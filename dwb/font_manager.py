"""
font.py

Description: Font creator for pygame that sets the font by font preferences
    or to the system font if none of the custom fonts are available on the
    system.

Created on Apr 24, 2017
"""


from pygame import font


class FontManager:
    """Manages creation of pygame fonts with custom font preferences."""
    def __init__(self, font_prefs: [str]=[]):
        """
        Initialize FontManager with a font preference list.

        Args:
            font_prefs(=[]): stores fonts names for preferred font types
                in descending order, where the first element is most
                preferred and the last element is least preferred
        """
        assert type(font_prefs) is list, \
            'FontManager.__init__: font_prefs expected ' + \
            '\'list\', got \'{}\''.format(str(type(font_prefs))[8:-2])
        for fnt in font_prefs:
            assert type(fnt) is str, \
                'FontManager.__init__: font_prefs elements expected ' + \
                '\'str\', got \'{}\''.format(str(type(fnt))[8:-2])
        self._font_prefs = font_prefs
        self._cached_fonts = {}
        self._cached_text = {}

    def __str__(self) -> str:
        return 'FontManager' + str(self._font_prefs) + '\n\t' + \
            'Cached Fonts' + '\n\t\t' + \
            '\n'.join(key for key in self._cached_fonts.keys()) + '\n\t' + \
            'Cached Text' + '\n\t\t' + \
            '\n'.join(key for key in self._cached_text.keys())

    def create_text(self, text, size,
                    color=(255, 255, 255),
                    bg=None,
                    bold: bool=False,
                    italics: bool=False) -> font.Font.render:
        key = '|'.join(map(str, (self._font_prefs, size, color, text)))
        # retrieve cached render if it exists
        image = self._cached_text.get(key, None)
        if image is None:
            font = self._get_font(size, bold, italics)
            image = font.render(text, True, color, bg)
            self._cached_text[key] = image
        return image

    def update_prefs(self, font_prefs: [str]) -> None:
        assert type(font_prefs) is list, \
            'FontManager.update_prefs: font_prefs expected ' + \
            '\'list\', got \'{}\''.format(str(type(font_prefs))[8:-2])
        for fnt in font_prefs:
            assert type(fnt) is str, \
                'FontManager.__init__: font_prefs elements expected ' + \
                '\'str\', got \'{}\''.format(str(type(fnt))[8:-2])
        self._font_prefs = font_prefs

    def _get_font(self, size: int,
                  bold: bool=False, italics: bool=False) -> font.Font:
        key = str(self._font_prefs) + '|' + str(size)
        font = self._cached_fonts.get(key, None)
        if not font:
            font = self._make_font(size, bold, italics)
            self._cached_fonts[key] = font
        return font

    def _make_font(self, size: int,
                   bold: bool=False,
                   italics: bool=False) -> font.Font:
        available = font.get_fonts()
        choices = map(lambda x: x.lower().replace(' ', ''), self._font_prefs)
        # font in preferences if available
        for choice in choices:
            if choice in available:
                return font.SysFont(choice, size, bold, italics)
        # default system font if no custom fonts not found
        return font.Font(None, size)
