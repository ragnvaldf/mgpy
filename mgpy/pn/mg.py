from .preconditions import SimplePreCondition
from .transition import Transition
from .place import Place, InitialPlace


class MarkedGraph(object):
    def __init__(self, actions):
        self.transitions = [Transition(action) for action in actions]

    def build(self):
        for transition in self.transitions:
            for precondition in transition.action.preconditions:
                if isinstance(precondition, SimplePreCondition):
                    place = Place(precondition.name, transition)

                    depending_transition = self.__find_transition_by_func(precondition.func)
                    depending_transition.dependents.append(transition)
                    depending_transition.output_places.append(place)
                else:
                    place = InitialPlace(precondition, transition)

                transition.input_places.append(place)

            if transition.has_token_in_each_input():
                transition.enable()

    def __find_transition_by_func(self, func):
        for transition in self.transitions:
            if transition.action.func == func:
                return transition
