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
