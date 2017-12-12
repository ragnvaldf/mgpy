from .transition import TState


class PN(object):
    def __init__(self, graph):
        self.graph = graph

    def get_enabled_transitions(self):
        return [transition_idx for transition_idx, transition_state in enumerate(self.graph.transition_states)
                if transition_state is TState.ENABLED]

    def start_firing(self, transition_idx):
        assert self.graph.get_transition_state(transition_idx) == TState.ENABLED
        self.graph.set_transition_state(transition_idx, TState.FIRING)

        input_places = self.graph.get_input_places(transition_idx)
        tokens = {self.graph.place_names[place_idx]: token for (place_idx, token) in
                  [(place_idx, self.graph.get_token_from_place(place_idx)) for place_idx in input_places]
                  if self.graph.is_real_place(place_idx)}
        func = self.graph.get_function_for_transition(transition_idx)

        return func, tokens

    def complete_firing(self, transition_idx, token):
        assert self.graph.get_transition_state(transition_idx) == TState.FIRING
        output_places = self.graph.get_output_places(transition_idx)
        [self.graph.deposit_token_in_place(token, place) for place in output_places]

        self.graph.set_transition_state(transition_idx, TState.DISABLED)
        enableable = self.graph.get_transitions_enabled_after(transition_idx)
        [self.graph.set_transition_state(transition, TState.ENABLED) for transition in enableable]

        return enableable
