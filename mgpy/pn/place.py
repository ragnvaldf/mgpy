class Place(object):
    def __init__(self, name, output_transition):
        self.name = name
        self.__tokens = []
        self.output_transition = output_transition

    def add_token(self, token):
        self.__tokens.append(token)

    def remove_token(self):
        assert len(self.__tokens) > 0, 'Tried removing non-existing token from {}'.format(self.name)

        return self.name, self.__tokens.pop(0)

    def token_count(self):
        return len(self.__tokens)

    def empty(self):
        return len(self.__tokens) == 0


class InitialPlace(Place):
    def __init__(self, siphon_precondition, output_transition):
        Place.__init__(self, siphon_precondition.name, output_transition)
        [Place.add_token(self, None) for _ in range(siphon_precondition.token_count)]

    def add_token(self, token):
        assert None, 'Initial place {} cannot store tokens'.format(self.name)

    def remove_token(self):
        Place.remove_token(self)

        return ()
