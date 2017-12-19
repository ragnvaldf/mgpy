from .pn import PN
from .functiontransition import FunctionTransition
from .deadtransition import DeadTransition
from .initialplace import InitialPlace
from .functionplace import FunctionPlace


class MGBuilder(object):
    def __init__(self):
        self.__actions = []
        self.__function_transitions = []
        self.__initial_places = []
        self.__requirement_places = []

    def add(self, action):
        self.__actions.append(action)

        return self

    def build(self):
        self.__make_places()
        self.__make_arcs()

        for transition in self.__function_transitions:
            if transition.can_be_enabled():
                transition.enable()

        return PN(self.__function_transitions)

    def __make_places(self):
        for action in self.__actions:
            output_transition = FunctionTransition(action.product(), action.get_func())
            self.__function_transitions.append(output_transition)

            if action.has_limit():
                dead_transition = DeadTransition()
                initial_place = InitialPlace(dead_transition, output_transition, action.limit())
                self.__initial_places.append(initial_place)

            for requirement in action.requirements():
                providers = [t for t in self.__function_transitions if requirement.satisfied_by(t.product())]
                assert len(providers) == 1, 'Exactly 1 provider must exist for {}'.format(requirement.product)
                input_transition = providers[0]

                requirement_place = FunctionPlace(input_transition, output_transition, requirement.product)
                self.__requirement_places.append(requirement_place)

    def __make_arcs(self):
        for place in self.__requirement_places:
            place.input_transition().add_output_place(place)
            place.output_transition().add_input_place(place)
        for place in self.__initial_places:
            place.input_transition().add_output_place(place)
            place.output_transition().add_input_place(place)
