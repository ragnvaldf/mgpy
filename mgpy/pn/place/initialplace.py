from .place import Place


class InitialPlace(Place):
    def __init__(self, input_transition, output_transition, token_count):
        Place.__init__(self, input_transition, output_transition, 'initial place')
        [Place.deposit(self, ()) for _ in range(token_count)]

    def deposit(self, token):
        assert None, 'Initial place for {} cannot store tokens'\
            .format(self.output_transition().product())

    def consume(self):
        return Place.consume(self)
