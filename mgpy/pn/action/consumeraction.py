from .action import Action
from ..place import FunctionPlace


class ConsumerAction(Action):
    def __init__(self, func, product, requirements):
        Action.__init__(self, func, product)
        self.__requirements = requirements

    def requirements(self):
        return self.__requirements

    # noinspection PyMethodOverriding
    def get_nodes(self, find_transition_satisfying):
        nodes = super().get_nodes()
        required_places = []
        for requirement in self.requirements():
            input_transition = find_transition_satisfying(requirement)
            requirement_place = FunctionPlace(input_transition, nodes['output_transition'], requirement.product)
            required_places.append(requirement_place)

        if len(required_places) > 0:
            nodes['required_places'] = required_places

        return nodes
