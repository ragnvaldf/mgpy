from .action import Action


class MockAction(Action):
    def __init__(self, func, provides, requirements, limit, mock):
        Action.__init__(self, func, provides, requirements, limit)
        self.__mock = mock

    def get_func(self):
        return self.__return_mock

    def __return_mock(self, **kwargs):
        return self.__mock
