from enum import IntEnum
from .preconditions import SimplePreCondition, SiphonPreCondition


class PN(object):
    def __init__(self, actions):
        self.actions = actions  # [transition_idx] = action
        self.action_count = len(actions)
        self.dependents = [[] for _ in range(self.action_count)]  # [dependency_idx] = [dependent_idx1...]
        self.places = []  # [place_idx] = [token1 token2...]
        self.place_names = []  # [place_idx] = 'name of dependency'
        self.siphons = []  # = [siphon1_place_idx siphon2_place_idx]
        self.transition_input_places = [[] for _ in range(self.action_count)]  # [transition_idx] = [place_idx1...]
        self.transition_output_places = [[] for _ in range(self.action_count)]  # [transition_idx] = [place_idx1...]
        self.transition_states = [TState.DISABLED]*self.action_count  # [transition_idx] = TState

    def build(self):
        for transition_idx in range(self.action_count):
            for precondition in self.actions[transition_idx].preconditions:
                if isinstance(precondition, SimplePreCondition):
                    assert precondition.func in [action.func for action in self.actions], \
                        '{} not defined as an action'.format(precondition.func.__name__)
                    dependency_idx = [action.func for action in self.actions].index(precondition.func)
                    place_idx = self.__make_place(precondition.name)

                    self.dependents[dependency_idx].append(transition_idx)
                    self.transition_input_places[transition_idx].append(place_idx)
                    self.transition_output_places[dependency_idx].append(place_idx)
                elif isinstance(precondition, SiphonPreCondition):
                    place_idx = self.__make_place(precondition.name)
                    [self.__deposit_token_in_place(None, place_idx) for _ in range(precondition.token_count)]
                    self.siphons.append(place_idx)
                    self.transition_input_places[transition_idx].append(place_idx)

    def get_state_dict(self):
        d = {}
        for transition_idx, action in enumerate(self.actions):
            d[action.name] = {}
            d[action.name]['State'] = str(self.transition_states[transition_idx])
            d[action.name]['Input'] = {}
            for place_idx in self.transition_input_places[transition_idx]:
                d[action.name]['Input'][self.place_names[place_idx]] = len(self.places[place_idx])

        return d

    def refresh_transition_states(self):
        for transition_idx in range(self.action_count):
            self.transition_states[transition_idx] = TState.ENABLED \
                if self.__can_fire(transition_idx) else TState.DISABLED

    def get_enabled_transitions(self):
        return [transition_idx for transition_idx, transition_state in enumerate(self.transition_states)
                if transition_state is TState.ENABLED]

    def start_firing(self, transition_idx):
        assert self.__get_transition_state(transition_idx) == TState.ENABLED
        self.__set_transition_state(transition_idx, TState.FIRING)

        input_places = self.__get_input_places(transition_idx)
        tokens = {self.place_names[place_idx]: token for (place_idx, token) in
                  [(place_idx, self.__get_token_from_place(place_idx)) for place_idx in input_places]
                  if self.__is_real_place(place_idx)}
        func = self.__get_function_for_transition(transition_idx)

        return func, tokens

    def complete_firing(self, transition_idx, token):
        assert self.__get_transition_state(transition_idx) == TState.FIRING
        output_places = self.__get_output_places(transition_idx)
        [self.__deposit_token_in_place(token, place) for place in output_places]

        self.__set_transition_state(transition_idx, TState.DISABLED)
        enableable = self.__get_transitions_enabled_after(transition_idx)
        [self.__set_transition_state(transition, TState.ENABLED) for transition in enableable]

        return enableable

    def __make_place(self, name):
        place_idx = len(self.places)
        self.places.append([])
        self.place_names.append(name)

        return place_idx

    def __get_transition_state(self, transition_idx):
        return self.transition_states[transition_idx]

    def __set_transition_state(self, transition_idx, state):
        self.transition_states[transition_idx] = state

    def __get_input_places(self, transition_idx):
        return self.transition_input_places[transition_idx]

    def __get_token_from_place(self, place_idx):
        return self.places[place_idx].pop(0)

    def __is_real_place(self, place_idx):
        return place_idx not in self.siphons

    def __get_function_for_transition(self, transition_idx):
        return self.actions[transition_idx].get_func()

    def __get_output_places(self, transition_idx):
        return self.transition_output_places[transition_idx]

    def __deposit_token_in_place(self, token, place_idx):
        self.places[place_idx].append(token)

    def __get_transitions_enabled_after(self, transition_idx):
        enableable = []
        if self.__can_fire(transition_idx):
            enableable.append(transition_idx)

        for dependent_idx in self.dependents[transition_idx]:
            if self.transition_states[dependent_idx] is TState.DISABLED and self.__can_fire(dependent_idx):
                enableable.append(dependent_idx)

        return enableable

    def __can_fire(self, transition_idx):
        input_places = self.__get_input_places(transition_idx)
        for place_idx in input_places:
            if len(self.places[place_idx]) == 0:  # Number of tokens available
                return False

        return True


class TState(IntEnum):
    DISABLED = 0
    ENABLED = 1
    FIRING = 2
