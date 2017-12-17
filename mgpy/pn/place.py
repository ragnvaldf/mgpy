class Place(object):
    def __init__(self, provided, output_transition):
        self.provided = provided
        self.output_transition = output_transition
        self.__tokens = []

    def deposit(self, token):
        self.__tokens.append(token)

    def consume(self):
        assert len(self.__tokens) > 0, 'Tried removing non-existing token for {} ({})'\
            .format(self.output_transition.action.real_func().__name__, self.provided)

        return self.provided, self.__tokens.pop(0)

    def token_count(self):
        return len(self.__tokens)

    def empty(self):
        return len(self.__tokens) == 0
