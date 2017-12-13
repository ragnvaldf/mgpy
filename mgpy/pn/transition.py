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

    def start_firing(self):
        self.__fire()
        func = self.action.get_func()
        tokens = dict([pair for pair in [place.remove_token() for place in self.input_places]
                       if len(pair) == 2])

        return func, tokens

    def complete_firing(self, token):
        self.__disable()
        [place.add_token(token) for place in self.output_places]
        enabled_transitions = [place.output_transition for place in self.output_places
                               if place.output_transition.try_enable()]

        if self.try_enable():
            enabled_transitions.append(self)

        return enabled_transitions

    def is_enabled(self):
        return self.__state == TState.ENABLED

    def is_disabled(self):
        return self.__state == TState.DISABLED

    def is_firing(self):
        return self.__state == TState.FIRING

    def __has_token_in_each_input(self):
        for place in self.input_places:
            if place.empty():  # Number of tokens available
                return False

        return True

    def __enable(self):
        assert self.__state is not TState.ENABLED, \
            'Illegal state change for transition {}: {} -> {}'\
                .format(self.action.name, str(self.__state), str(TState.ENABLED))
        self.__state = TState.ENABLED

    def __disable(self):
        assert self.__state is TState.FIRING, \
            'Illegal state change for transition {}: {} -> {}'\
                .format(self.action.name, str(self.__state), str(TState.DISABLED))
        self.__state = TState.DISABLED

    def __fire(self):
        assert self.__state is TState.ENABLED, \
            'Illegal state change for transition {}: {} -> {}'\
                .format(self.action.name, str(self.__state), str(TState.FIRING))
        self.__state = TState.FIRING


class TState(IntEnum):
    DISABLED = 0
    ENABLED = 1
    FIRING = 2
