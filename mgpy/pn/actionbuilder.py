from mgpy.pn.preconditions import SimplePreCondition, SiphonPreCondition
from mgpy.pn.actions import Action, MockAction


class ActionBuilder(object):
    def __init__(self, func):
        assert callable(func)
        self.__func = func  # Actions are transitions
        self.__preconditions = []  # Preconditions are places
        self.__mock_object = None

    def precondition(self, func, name=None):
        assert func is not None
        if name is None:
            name = func.__name__

        self.__preconditions.append(SimplePreCondition(func, name))

        return self

    def mock(self, mock_object):
        self.__mock_object = mock_object

        return self

    def once(self):
        return self.max_runs(1)

    def max_runs(self, max_runs):
        assert max_runs > 0
        self.__preconditions.append(SiphonPreCondition(max_runs))

        return self

    def build(self):
        if self.__mock_object is None:
            return Action(self.__func, self.__preconditions)
        else:
            return MockAction(self.__func, self.__preconditions, self.__mock_object)
