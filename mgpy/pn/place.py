class Place(object):
    def __init__(self, provided, input_transition, output_transition):
        self.provided = provided
        self.input_transition = input_transition
        self.output_transition = output_transition
        self.__tokens = []

    def deposit(self, token):
        self.__tokens.append(token)

    def consume(self):
        assert len(self.__tokens) > 0, 'Tried removing non-existing token({}) for {}'\
            .format(self.provided, self.output_transition.product())

        return self.provided, self.__tokens.pop(0)

    def token_count(self):
        return len(self.__tokens)

    def empty(self):
        return len(self.__tokens) == 0
