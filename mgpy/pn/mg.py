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

            if self.__can_fire(transition):
                transition.enable()

    def get_state_dict(self):
        d = {}
        for transition_idx, transition in enumerate(self.transitions):
            d[transition.action.name] = {}
            d[transition.action.name]['State'] = str(transition.state())
            for place in transition.input_places:
                d[transition.action.name][place.name] = place.token_count()

        return d

    def get_enabled_transitions(self):
        return [transition for transition in self.transitions if transition.enabled()]

    def get_transitions_enabled_after(self, transition):
        enableable = [depending_transition for depending_transition in transition.dependents
                      if depending_transition.disabled() and self.__can_fire(depending_transition)]

        if self.__can_fire(transition):
            enableable.append(transition)

        return enableable

    def __can_fire(self, transition):
        for place in transition.input_places:
            if place.empty():  # Number of tokens available
                return False

        return True

    def __find_transition_by_func(self, func):
        for transition in self.transitions:
            if transition.action.func == func:
                return transition
