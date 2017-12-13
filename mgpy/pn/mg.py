from .preconditions import SimplePreCondition, SiphonPreCondition
from .transition import Transition, TState
from .place import Place, InitialPlace


class MarkedGraph(object):
    def __init__(self, actions):
        self.transitions = [Transition(action, idx) for idx, action in enumerate(actions)]
        self.places = []  # [place_idx] = place

    def build(self):
        for transition in self.transitions:
            for precondition in transition.action.preconditions:
                if isinstance(precondition, SimplePreCondition):
                    place = Place(precondition.name)

                    depending_transition = self.__find_transition_by_func(precondition.func)
                    depending_transition.dependents.append(transition)
                    depending_transition.output_places.append(place)
                elif isinstance(precondition, SiphonPreCondition):
                    place = InitialPlace(precondition)

                self.places.append(place)
                transition.input_places.append(place)

    def refresh_transition_states(self):
        for transition in self.transitions:
            if self.__can_fire(transition):
                transition.enable()

    def get_state_dict(self):
        d = {}
        for transition_idx, transition in enumerate(self.transitions):
            d[transition.action.name] = {}
            d[transition.action.name]['State'] = str(transition.state())
            d[transition.action.name]['Input'] = {}
            for place_idx in transition.input_places:
                d[transition.action.name]['Input'][self.places[place_idx].name] = self.places[place_idx].token_count()

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
