from .initialplace import InitialPlace


class PN(object):
    def __init__(self, transitions):
        self.transitions = transitions

    def get_enabled_transitions(self):
        return [transition for transition in self.transitions if transition.is_enabled()]

    def get_state_dict(self):
        d = {}
        for transition in self.transitions:
            d[transition.name()] = {}
            d[transition.name()]['State'] = str(transition.state())
            for place in transition.input_places():
                if isinstance(place, InitialPlace):
                    d[transition.name()]['initial'] = place.token_count()
                else:
                    d[transition.name()][place.provided] = place.token_count()

        return d


def start_firing(transition):
    transition.fire()
    func = transition.action.get_func()
    tokens = consume_tokens(transition.input_places())

    return func, tokens


def complete_firing(transition, token):
    transition.disable()
    deposit(token, transition.output_places())

    enabled_transitions = try_enable_output_transitions(transition.output_places())
    if transition.try_enable():
        enabled_transitions.append(transition)

    return enabled_transitions


def deposit(token, output_places):
    [place.add_token(token) for place in output_places]


def consume_tokens(input_places):
    return dict([pair for pair in [place.remove_token() for place in input_places] if len(pair) == 2])


def try_enable_output_transitions(list_of_places):
    return [place.output_transition for place in list_of_places if place.output_transition.try_enable()]
