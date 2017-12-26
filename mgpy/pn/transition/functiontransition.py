from .transition import Transition
from ..state import ColoredToken


class FunctionTransition(Transition):
    def __init__(self, product, func):
        Transition.__init__(self, '{} -> {}'.format(func.__name__, product))
        self.__product = product
        self.__func = func

    def product(self):
        return self.__product

    def func(self):
        return self.__func

    def run_function(self, input_tokens, firing_complete):
        output_token = self.func()(**argument_dict_from_tokens(input_tokens))
        firing_complete(self, output_token)


def argument_dict_from_tokens(tokens):
    return {name: value
            for colored_token in filter(lambda token: isinstance(token, ColoredToken), tokens)
            for (name, value) in colored_token.colors()}
