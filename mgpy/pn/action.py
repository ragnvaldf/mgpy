from .functiontransition import FunctionTransition


class Action(object):
    def __init__(self, func, product, requirements, limit):
        self.__func = func
        self.__product = product
        self.__requirements = requirements
        self.__limit = limit

    def get_func(self):
        return self.__func

    def real_func(self):
        return self.__func

    def provides(self, requirement):
        return self.__product == requirement.provider

    def product(self):
        return self.__product

    def requirements(self):
        return self.__requirements

    def has_limit(self):
        return self.__limit is not None

    def limit(self):
        return self.__limit

    def to_transition(self):
        return FunctionTransition(self)
