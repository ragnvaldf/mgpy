from .token import Token
from .tokencolors import TokenColors


class ColoredToken(Token):
    def __init__(self, colors):
        super().__init__()
        self.__colors = TokenColors(colors)

    def colors(self):
        return self.__colors
