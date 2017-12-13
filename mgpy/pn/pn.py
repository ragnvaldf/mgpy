class PN(object):
    def __init__(self, graph):
        self.graph = graph

    def get_enabled_transitions(self):
        return self.graph.get_enabled_transitions()

    def start_firing(self, transition):
        transition.fire()
        func = transition.action.get_func()
        input_places = self.graph.get_input_places(transition)
        tokens = dict([pair for pair in self.__get_tokens_from_places(input_places) if len(pair) == 2])

        return func, tokens

    def complete_firing(self, transition, token):
        output_places = self.graph.get_output_places(transition)
        [self.graph.deposit_token_in_place(token, place) for place in output_places]

        transition.disable()
        enableable = self.graph.get_transitions_enabled_after(transition)
        [enableable_transition.enable() for enableable_transition in enableable]

        return enableable

    def __get_tokens_from_places(self, input_places):
        return [self.graph.get_token_from_place(place_idx) for place_idx in input_places]
