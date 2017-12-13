from .preconditions import SimplePreCondition, SiphonPreCondition
from .transition import Transition, TState
from .place import Place, InitialPlace


class MarkedGraph(object):
    def __init__(self, actions):
        self.transitions = [Transition(action, idx) for idx, action in enumerate(actions)]
        self.places = []  # [place_idx] = place
        self.action_count = len(actions)
        self.dependents = [[] for _ in range(self.action_count)]  # [dependency_idx] = [dependent_idx1...]
        self.transition_input_places = [[] for _ in range(self.action_count)]  # [transition_idx] = [place_idx1...]
        self.transition_output_places = [[] for _ in range(self.action_count)]  # [transition_idx] = [place_idx1...]

    def build(self):
        for transition_idx in range(self.action_count):
            for precondition in self.transitions[transition_idx].action.preconditions:
                place_idx = len(self.places)  # Each precondition requires a place to store tokens
                self.transition_input_places[transition_idx].append(place_idx)

                if isinstance(precondition, SimplePreCondition):
                    self.places.append(Place(precondition.name))

                    dependency_idx = [transition.action.func for transition in self.transitions].index(precondition.func)
                    self.dependents[dependency_idx].append(transition_idx)
                    self.transition_output_places[dependency_idx].append(place_idx)
                elif isinstance(precondition, SiphonPreCondition):
                    self.places.append(InitialPlace(precondition))

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
            for place_idx in self.transition_input_places[transition_idx]:
                d[transition.action.name]['Input'][self.places[place_idx].name] = self.places[place_idx].token_count()

        return d

    def get_enabled_transitions(self):
        return [transition for transition in self.transitions if transition.enabled()]

    def get_input_places(self, transition):
        return self.transition_input_places[transition.idx]

    def get_token_from_place(self, place_idx):
        return self.places[place_idx].remove_token()

    def get_output_places(self, transition):
        return self.transition_output_places[transition.idx]

    def deposit_token_in_place(self, token, place_idx):
        self.places[place_idx].add_token(token)

    def get_transitions_enabled_after(self, transition):
        enableable = []
        if self.__can_fire(transition):
            enableable.append(transition)

        for dependent_idx in self.dependents[transition.idx]:
            if self.transitions[dependent_idx].disabled() and self.__can_fire(self.transitions[dependent_idx]):
                enableable.append(self.transitions[dependent_idx])

        return enableable

    def __can_fire(self, transition):
        input_places = self.get_input_places(transition)
        for place_idx in input_places:
            if self.places[place_idx].empty():  # Number of tokens available
                return False

        return True
