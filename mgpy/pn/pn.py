class PN(object):
    def __init__(self, transitions):
        self.transitions = transitions

    def get_enabled_transitions(self):
        return [transition for transition in self.transitions if transition.is_enabled()]

    def get_state_dict(self):
        d = {}
        for transition in self.transitions:
            d[transition.action.name] = {}
            d[transition.action.name]['State'] = str(transition.state())
            for place in transition.input_places:
                d[transition.action.name][place.name] = place.token_count()

        return d


def start_firing(transition):
    transition.fire()
    func = transition.action.get_func()
    tokens = dict([pair for pair in [place.remove_token() for place in transition.input_places]
                   if len(pair) == 2])

    return func, tokens


def complete_firing(transition, token):
    transition.disable()
    [place.add_token(token) for place in transition.output_places]
    enabled_transitions = [place.output_transition for place in transition.output_places
                           if place.output_transition.try_enable()]

    if transition.try_enable():
        enabled_transitions.append(transition)

    return enabled_transitions
