from enum import IntEnum


class Transition(object):
    def __init__(self, name):
        self.__name = name
        self.__input_places = []
        self.__output_places = []
        self.__state = TState.DISABLED

    def add_input_place(self, place):
        self.__input_places.append(place)

    def add_output_place(self, place):
        self.__output_places.append(place)

    def input_places(self):
        return self.__input_places

    def output_places(self):
        return self.__output_places

    def can_be_enabled(self):
        return not self.is_enabled() and self.__has_token_in_each_input()

    def __has_token_in_each_input(self):
        for place in self.input_places():
            if place.empty():
                return False

        return True

    def state(self):
        return self.__state

    def name(self):
        return self.__name

    def is_enabled(self):
        return self.__state is TState.ENABLED

    def is_disabled(self):
        return self.__state is TState.DISABLED

    def is_firing(self):
        return self.__state is TState.FIRING

    def fire(self):
        assert self.__state is TState.ENABLED, \
            'Illegal state change for transition {}: {} -> {}'\
            .format(self.__name, str(self.__state), str(TState.FIRING))
        self.__state = TState.FIRING

    def disable(self):
        assert self.__state is TState.FIRING, \
            'Illegal state change for transition {}: {} -> {}'\
            .format(self.__name, str(self.__state), str(TState.DISABLED))
        self.__state = TState.DISABLED

    def enable(self):
        assert self.__state is not TState.ENABLED, \
            'Illegal state change for transition {}: {} -> {}'\
            .format(self.__name, str(self.__state), str(TState.ENABLED))
        self.__state = TState.ENABLED


class TState(IntEnum):
    DISABLED = 0
    ENABLED = 1
    FIRING = 2
