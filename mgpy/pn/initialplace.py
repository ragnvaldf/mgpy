from .place import Place


class InitialPlace(Place):
    def __init__(self, output_transition):
        Place.__init__(self, None, output_transition)
        [Place.deposit(self, None) for _ in range(output_transition.action.limit())]

    def deposit(self, token):
        assert None, 'Initial place for {} cannot store tokens'\
            .format(self.output_transition.action.real_func().__name__)

    def consume(self):
        Place.consume(self)

        return ()
