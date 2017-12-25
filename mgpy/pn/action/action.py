from mgpy.pn.transition.functiontransition import FunctionTransition


class Action(object):
    def __init__(self, func, product):
        self.__func = func
        self.__real_func = func
        self.__product = product
        self.__mock_object = None

    def func(self):
        return self.__func

    def real_func(self):
        return self.__real_func

    def product(self):
        return self.__product

    def set_mock(self, mock_object):
        self.__mock_object = mock_object
        self.__func = self.__mock

    # noinspection PyUnusedLocal
    def __mock(self, **kwargs):
        return self.__mock_object

    def get_nodes(self):
        return {
            'output_transition': FunctionTransition(self.product(), self.func())
        }
