from .place import Place


class InitialPlace(Place):
    def __init__(self, output_transition, token_count):
        Place.__init__(self, 'Dummy', None, output_transition)
        [Place.deposit(self, None) for _ in range(token_count)]

    def deposit(self, token):
        assert None, 'Initial place for {} cannot store tokens'\
            .format(self.output_transition.product())

    def consume(self):
        Place.consume(self)

        return ()
