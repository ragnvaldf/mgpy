from .preconditions import SimplePreCondition, SiphonPreCondition
from .transition import Transition, TState
from .place import Place, InitialPlace


class MarkedGraph(object):
    def __init__(self, actions):
        self.transitions = [Transition(action, idx) for idx, action in enumerate(actions)]
        self.places = []  # [place_idx] = place
        self.dependents = [[] for _ in range(len(actions))]  # [dependency_idx] = [dependent_idx1...]

    def build(self):
        for transition in self.transitions:
            for precondition in transition.action.preconditions:
                if isinstance(precondition, SimplePreCondition):
                    place = Place(precondition.name)

                    dependency_idx = [transition.action.func for transition in self.transitions].index(precondition.func)
                    self.dependents[dependency_idx].append(transition.idx)
                    self.transitions[dependency_idx].output_places.append(place)
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
        enableable = []
        if self.__can_fire(transition):
            enableable.append(transition)

        for dependent_idx in self.dependents[transition.idx]:
            if self.transitions[dependent_idx].disabled() and self.__can_fire(self.transitions[dependent_idx]):
                enableable.append(self.transitions[dependent_idx])

        return enableable

    def __can_fire(self, transition):
        for place in transition.input_places:
            if place.empty():  # Number of tokens available
                return False

        return True
