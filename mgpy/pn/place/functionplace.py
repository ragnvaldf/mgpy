from mgpy.pn.place import Place


class FunctionPlace(Place):
    def __init__(self, input_transition, output_transition, provided):
        Place.__init__(self, input_transition, output_transition, provided)
        self.__provided = provided

    def deposit(self, token):
        Place.deposit(self, token)

    def consume(self):
        return self.__provided, Place.consume(self)

    def provided(self):
        return self.__provided
