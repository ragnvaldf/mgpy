from .transition import Transition


class DeadTransition(Transition):
    def __init__(self):
        Transition.__init__(self, 'dead transition')

    def can_be_enabled(self):
        return False
