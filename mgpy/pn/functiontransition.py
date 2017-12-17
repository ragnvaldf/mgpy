from .transition import Transition


class FunctionTransition(Transition):
    def __init__(self, action):
        Transition.__init__(self, action.product())
        self.action = action
