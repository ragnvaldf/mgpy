from .place import Place


class InitialPlace(Place):
    def __init__(self, output_transition):
        Place.__init__(self, None, output_transition)
        [Place.add_token(self, None) for _ in range(output_transition.action.limit())]

    def add_token(self, token):
        assert None, 'Initial place for {} cannot store tokens'\
            .format(self.output_transition.action.real_func().__name__)

    def remove_token(self):
        Place.remove_token(self)

        return ()
