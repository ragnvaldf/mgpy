from enum import IntEnum


class Transition(object):
    def __init__(self, action):
        self.action = action
        self.input_places = []
        self.output_places = []
        self.__state = TState.DISABLED

    def try_enable(self):
        if self.is_disabled() and self.__has_token_in_each_input():
            self.__enable()
            return True

        return False

    def get_state(self):
        return self.__state

    def is_enabled(self):
        return self.__state == TState.ENABLED

    def is_disabled(self):
        return self.__state == TState.DISABLED

    def is_firing(self):
        return self.__state == TState.FIRING

    def fire(self):
        assert self.__state is TState.ENABLED, \
            'Illegal state change for transition {}: {} -> {}'\
            .format(self.action.name, str(self.__state), str(TState.FIRING))
        self.__state = TState.FIRING

    def disable(self):
        assert self.__state is TState.FIRING, \
            'Illegal state change for transition {}: {} -> {}'\
            .format(self.action.name, str(self.__state), str(TState.DISABLED))
        self.__state = TState.DISABLED

    def __enable(self):
        assert self.__state is not TState.ENABLED, \
            'Illegal state change for transition {}: {} -> {}'\
            .format(self.action.name, str(self.__state), str(TState.ENABLED))
        self.__state = TState.ENABLED

    def __has_token_in_each_input(self):
        for place in self.input_places:
            if place.empty():  # Number of tokens available
                return False

        return True


class TState(IntEnum):
    DISABLED = 0
    ENABLED = 1
    FIRING = 2
