from ..state import Token


class Place(object):
    def __init__(self, input_transition, output_transition, name):
        self.__name = name
        self.__input_transition = input_transition
        self.__output_transition = output_transition
        self.__tokens = []

    def name(self):
        return self.__name

    def deposit(self, token):
        assert isinstance(token, Token)
        self.__tokens.append(token)

    def consume(self):
        assert len(self.__tokens) > 0, 'Tried removing non-existing token({}) for {}'\
            .format(self.__name, self.output_transition().product())

        return self.__tokens.pop(0)

    def token_count(self):
        return len(self.__tokens)

    def empty(self):
        return len(self.__tokens) == 0

    def input_transition(self):
        return self.__input_transition

    def output_transition(self):
        return self.__output_transition
