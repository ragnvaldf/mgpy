from .consumeraction import ConsumerAction
from ..transition import DeadTransition
from ..place import InitialPlace


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
            nodes['initial_place'] = InitialPlace(nodes['input_transition'], nodes['output_transition'], self.limit())

        return nodes
