from enum import IntEnum


class TState(IntEnum):
    DISABLED = 0
    ENABLED = 1
    FIRING = 2


class Transition(object):
    def __init__(self, action):
        self.action = action
        self.__state = TState.DISABLED

    def enable(self):
        self.__state = TState.ENABLED

    def disable(self):
        self.__state = TState.DISABLED

    def fire(self):
        self.__state = TState.FIRING

    def enabled(self):
        return self.__state == TState.ENABLED

    def disabled(self):
        return self.__state == TState.DISABLED

    def firing(self):
        return self.__state == TState.FIRING

    def state(self):
        return self.__state
