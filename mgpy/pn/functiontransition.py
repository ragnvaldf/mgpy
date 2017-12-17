from .transition import Transition


class FunctionTransition(Transition):
    def __init__(self, action):
        Transition.__init__(self, action.product())
        self.action = action

    def try_enable(self):
        if self.is_disabled() and self.__has_token_in_each_input():
            self.enable()
            return True

        return False

    def __has_token_in_each_input(self):
        for place in self.input_places():
            if place.empty():  # Number of tokens available
                return False

        return True
