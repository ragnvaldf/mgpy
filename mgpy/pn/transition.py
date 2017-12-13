from enum import IntEnum


class TState(IntEnum):
    DISABLED = 0
    ENABLED = 1
    FIRING = 2


class Transition(object):
    def __init__(self, action, transition_idx):
        self.action = action
        self.idx = transition_idx
        self.__state = TState.DISABLED

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
