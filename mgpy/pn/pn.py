class PN(object):
    def __init__(self, graph):
        self.graph = graph

    def get_enabled_transitions(self):
        return [transition for transition in self.graph.transitions if transition.enabled()]

    def get_state_dict(self):
        d = {}
        for transition in self.graph.transitions:
            d[transition.action.name] = {}
            d[transition.action.name]['State'] = str(transition.state())
            for place in transition.input_places:
                d[transition.action.name][place.name] = place.token_count()

        return d

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
