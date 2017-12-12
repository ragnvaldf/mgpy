from .preconditions import SimplePreCondition, SiphonPreCondition
from .transition import TState


class MarkedGraph(object):
    def __init__(self, actions):
        self.actions = actions  # [transition_idx] = action
        self.action_count = len(actions)
        self.dependents = [[] for _ in range(self.action_count)]  # [dependency_idx] = [dependent_idx1...]
        self.places = []  # [place_idx] = [token1 token2...]
        self.place_names = []  # [place_idx] = 'name of dependency'
        self.siphons = []  # = [siphon1_place_idx siphon2_place_idx]
        self.transition_input_places = [[] for _ in range(self.action_count)]  # [transition_idx] = [place_idx1...]
        self.transition_output_places = [[] for _ in range(self.action_count)]  # [transition_idx] = [place_idx1...]
        self.transition_states = [TState.DISABLED] * self.action_count  # [transition_idx] = TState

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
                    [self.deposit_token_in_place(None, place_idx) for _ in range(precondition.token_count)]
                    self.siphons.append(place_idx)
                    self.transition_input_places[transition_idx].append(place_idx)

    def refresh_transition_states(self):
        for transition_idx in range(self.action_count):
            self.transition_states[transition_idx] = TState.ENABLED \
                if self.__can_fire(transition_idx) else TState.DISABLED

    def get_state_dict(self):
        d = {}
        for transition_idx, action in enumerate(self.actions):
            d[action.name] = {}
            d[action.name]['State'] = str(self.transition_states[transition_idx])
            d[action.name]['Input'] = {}
            for place_idx in self.transition_input_places[transition_idx]:
                d[action.name]['Input'][self.place_names[place_idx]] = len(self.places[place_idx])

        return d

    def __make_place(self, name):
        place_idx = len(self.places)
        self.places.append([])
        self.place_names.append(name)

        return place_idx

    def get_transition_state(self, transition_idx):
        return self.transition_states[transition_idx]

    def set_transition_state(self, transition_idx, state):
        self.transition_states[transition_idx] = state

    def get_input_places(self, transition_idx):
        return self.transition_input_places[transition_idx]

    def get_token_from_place(self, place_idx):
        return self.places[place_idx].pop(0)

    def is_real_place(self, place_idx):
        return place_idx not in self.siphons

    def get_function_for_transition(self, transition_idx):
        return self.actions[transition_idx].get_func()

    def get_output_places(self, transition_idx):
        return self.transition_output_places[transition_idx]

    def deposit_token_in_place(self, token, place_idx):
        self.places[place_idx].append(token)

    def get_transitions_enabled_after(self, transition_idx):
        enableable = []
        if self.__can_fire(transition_idx):
            enableable.append(transition_idx)

        for dependent_idx in self.dependents[transition_idx]:
            if self.transition_states[dependent_idx] is TState.DISABLED and self.__can_fire(dependent_idx):
                enableable.append(dependent_idx)

        return enableable

    def __can_fire(self, transition_idx):
        input_places = self.get_input_places(transition_idx)
        for place_idx in input_places:
            if len(self.places[place_idx]) == 0:  # Number of tokens available
                return False

        return True
