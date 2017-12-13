from enum import IntEnum


class TState(IntEnum):
    DISABLED = 0
    ENABLED = 1
    FIRING = 2


class Transition(object):
    def __init__(self, action):
        self.action = action
        self.__state = TState.DISABLED
        self.input_places = []
        self.output_places = []
        self.dependents = []

    def enable(self):
        assert self.__state is not TState.ENABLED, \
            'Illegal state change for transition {}: {} -> {}'.format(self.action.name, self.__state, TState.ENABLED)
        self.__state = TState.ENABLED

    def disable(self):
        assert self.__state is TState.FIRING, \
            'Illegal state change for transition {}: {} -> {}'.format(self.action.name, self.__state, TState.DISABLED)
        self.__state = TState.DISABLED

    def fire(self):
        assert self.__state is TState.ENABLED, \
            'Illegal state change for transition {}: {} -> {}'.format(self.action.name, self.__state, TState.FIRING)
        self.__state = TState.FIRING

    def enabled(self):
        return self.__state == TState.ENABLED

    def disabled(self):
        return self.__state == TState.DISABLED

    def firing(self):
        return self.__state == TState.FIRING

    def state(self):
        return self.__state

    def has_token_in_each_input(self):
        for place in self.input_places:
            if place.empty():  # Number of tokens available
                return False

        return True
