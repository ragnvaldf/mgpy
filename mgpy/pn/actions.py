class Action(object):
    def __init__(self, func, preconditions):
        self.name = func.__name__
        self.func = func
        self.preconditions = preconditions

    def get_func(self):
        return self.func


class MockAction(Action):
    def __init__(self, func, preconditions, mock):
        Action.__init__(self, func, preconditions)
        self.__mock = mock

    def get_func(self):
        return self.__return_mock

    def __return_mock(self, **kwargs):
        return self.__mock
