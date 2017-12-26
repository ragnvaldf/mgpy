from .consumeraction import ConsumerAction
from ..transition import DeadTransition
from ..place import Place
from ..state import Token


class FunctionAction(ConsumerAction):
    def __init__(self, func, product, requirements, limit):
        ConsumerAction.__init__(self, func, product, requirements)
        self.__limit = limit

    def has_limit(self):
        return self.__limit is not None

    def limit(self):
        return self.__limit

    def get_nodes(self, find_transition_satisfying):
        nodes = super().get_nodes(find_transition_satisfying)
        if self.has_limit():
            nodes['input_transition'] = DeadTransition()
            initial_place = Place(nodes['input_transition'], nodes['output_transition'],
                                           'limit={}'.format(self.limit()))
            [initial_place.deposit(Token()) for _ in range(self.limit())]
            nodes['initial_place'] = initial_place

        return nodes
