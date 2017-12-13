class PN(object):
    def __init__(self, graph):
        self.graph = graph

    def get_enabled_transitions(self):
        return self.graph.get_enabled_transitions()

    def start_firing(self, transition):
        transition.fire()
        func = transition.action.get_func()
        tokens = dict([pair for pair in [place.remove_token() for place in transition.input_places]
                       if len(pair) == 2])

        return func, tokens

    def complete_firing(self, transition, token):
        [place.add_token(token) for place in transition.output_places]

        transition.disable()
        enableable = self.graph.get_transitions_enabled_after(transition)
        [enableable_transition.enable() for enableable_transition in enableable]

        return enableable
