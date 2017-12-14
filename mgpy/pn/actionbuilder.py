from .requirement import Requirement
from .action import Action
from .mockaction import MockAction


class ActionBuilder(object):
    def __init__(self, func):
        assert callable(func)
        self .__func = func
        self.__requirements = []
        self.__provides = None
        self.__limit = None
        self.__mock_object = None

    def read_annotations(self):
        for k, v in self.__func.__annotations__.items():
            if k == 'return':
                self.provides(v)
            else:
                self.requires(v)

        return self

    def requires(self, provider):
        if callable(provider):
            provider = provider.__name__
        else:
            assert isinstance(provider, str), 'Requirement must be identified by function or string'

        self.__requirements.append(Requirement(provider))

        return self

    def provides(self, p):
        self.__provides = p

        return self

    def mock(self, mock_object):
        self.__mock_object = mock_object

        return self

    def once(self):
        return self.limit(1)

    def limit(self, limit):
        assert limit > 0
        self.__limit = limit

        return self

    def build(self):
        if self.__provides is None:
            self.__provides = self.__func.__name__

        if self.__mock_object is None:
            return Action(self.__func, self.__provides, self.__requirements, self.__limit)
        else:
            return MockAction(self.__func, self.__provides, self.__requirements, self.__limit, self.__mock_object)
