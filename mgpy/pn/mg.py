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
                    place = Place(precondition.name)

                    depending_transition = self.__find_transition_by_func(precondition.func)
                    depending_transition.dependents.append(transition)
                    depending_transition.output_places.append(place)
                else:
                    place = InitialPlace(precondition)

                transition.input_places.append(place)

            if transition.has_token_in_each_input():
                transition.enable()

    def get_transitions_enabled_after(self, transition):
        enableable = [depending_transition for depending_transition in transition.dependents
                      if depending_transition.disabled() and depending_transition.has_token_in_each_input()]

        if transition.has_token_in_each_input():
            enableable.append(transition)

        return enableable

    def __find_transition_by_func(self, func):
        for transition in self.transitions:
            if transition.action.func == func:
                return transition
