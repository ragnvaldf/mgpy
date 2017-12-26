from .coloredtoken import ColoredToken


class Provide(ColoredToken):
    def __init__(self, single_state):
        super().__init__([single_state])
