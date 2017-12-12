class Action(object):
    def __init__(self, func, preconditions):
        self.name = func.__name__
        self.func = func
        self.preconditions = preconditions

    def get_func(self):
        return self.func

    def __hash__(self):
        return hash((self.name, self.func, self.preconditions))

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return (self.name, self.func, self.preconditions) == (other.name, other.func, other.preconditions)

        return NotImplemented

    def __str__(self):
        return '{}({})'.format(self.func.__name__, '-'.join([p.__name__ for p in self.preconditions]))

    __repr__ = __str__


class MockAction(Action):
    def __init__(self, func, preconditions, mock):
        Action.__init__(self, func, preconditions)
        self.__mock = mock

    def get_func(self):
        return self.__return_mock

    def __return_mock(self, **kwargs):
        return self.__mock
