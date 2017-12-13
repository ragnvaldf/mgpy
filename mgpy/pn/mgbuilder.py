from .pn import PN
from .preconditions import SimplePreCondition
from .transition import Transition
from .place import Place, InitialPlace


class MGBuilder(object):
    def __init__(self):
        self.actions = []

    def add(self, action):
        self.actions.append(action)

        return self

    def build(self):
        transitions = [Transition(action) for action in self.actions]
        for transition in transitions:
            for precondition in transition.action.preconditions:
                if isinstance(precondition, SimplePreCondition):
                    place = Place(precondition.name, transition)

                    depending_transition = self.__find_transition_by_func(precondition.func, transitions)
                    depending_transition.output_places.append(place)
                else:
                    place = InitialPlace(precondition, transition)

                transition.input_places.append(place)

            transition.try_enable()

        return PN(transitions)

    def __find_transition_by_func(self, func, transitions):
        for transition in transitions:
            if transition.action.func == func:
                return transition
