from .transition import Transition


class FunctionTransition(Transition):
    def __init__(self, product, func):
        Transition.__init__(self, product)
        self.func = func

    def run_function(self, input_tokens):
        return self.func(**argument_dict_from_tokens(input_tokens))


def argument_dict_from_tokens(tokens):
    return dict([pair for pair in tokens if len(pair) == 2])
