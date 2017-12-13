from .preconditions import SimplePreCondition, SiphonPreCondition
from .transition import Transition, TState
from .place import Place, InitialPlace


class MarkedGraph(object):
    def __init__(self, actions):
        self.transitions = [Transition(action) for action in actions]  # [transition_idx] = transition
        self.places = []  # [place_idx] = place
        self.action_count = len(actions)
        self.dependents = [[] for _ in range(self.action_count)]  # [dependency_idx] = [dependent_idx1...]
        self.transition_input_places = [[] for _ in range(self.action_count)]  # [transition_idx] = [place_idx1...]
        self.transition_output_places = [[] for _ in range(self.action_count)]  # [transition_idx] = [place_idx1...]

    def build(self):
        for transition_idx in range(self.action_count):
            for precondition in self.transitions[transition_idx].action.preconditions:
                if isinstance(precondition, SimplePreCondition):
                    assert precondition.func in [transition.action.func for transition in self.transitions], \
                        '{} not defined as an action'.format(precondition.func.__name__)
                    dependency_idx = [transition.action.func for transition in self.transitions].index(precondition.func)
                    place_idx = self.__make_place(precondition.name)

                    self.dependents[dependency_idx].append(transition_idx)
                    self.transition_input_places[transition_idx].append(place_idx)
                    self.transition_output_places[dependency_idx].append(place_idx)
                elif isinstance(precondition, SiphonPreCondition):
                    place_idx = self.__make_place(precondition.name, precondition.token_count)
                    self.transition_input_places[transition_idx].append(place_idx)

    def refresh_transition_states(self):
        for transition_idx, transition in enumerate(self.transitions):
            if self.__can_fire(transition_idx):
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
        return [transition_idx for transition_idx, transition in enumerate(self.transitions) if transition.enabled()]

    def __make_place(self, name, token_count=None):
        place_idx = len(self.places)
        if token_count is None:
            self.places.append(Place(name))
        else:
            self.places.append(InitialPlace(name, token_count))

        return place_idx

    def get_transition_state(self, transition_idx):
        return self.transitions[transition_idx].state()

    def set_transition_state(self, transition_idx, state):
        if state is TState.ENABLED:
            self.transitions[transition_idx].enable()
        elif state is TState.DISABLED:
            self.transitions[transition_idx].disable()
        elif state is TState.FIRING:
            self.transitions[transition_idx].fire()

    def get_input_places(self, transition_idx):
        return self.transition_input_places[transition_idx]

    def get_token_from_place(self, place_idx):
        return self.places[place_idx].remove_token()

    def get_function_for_transition(self, transition_idx):
        return self.transitions[transition_idx].action.get_func()

    def get_output_places(self, transition_idx):
        return self.transition_output_places[transition_idx]

    def deposit_token_in_place(self, token, place_idx):
        self.places[place_idx].add_token(token)

    def get_transitions_enabled_after(self, transition_idx):
        enableable = []
        if self.__can_fire(transition_idx):
            enableable.append(transition_idx)

        for dependent_idx in self.dependents[transition_idx]:
            if self.transitions[dependent_idx].disabled() and self.__can_fire(dependent_idx):
                enableable.append(dependent_idx)

        return enableable

    def __can_fire(self, transition_idx):
        input_places = self.get_input_places(transition_idx)
        for place_idx in input_places:
            if self.places[place_idx].empty():  # Number of tokens available
                return False

        return True
