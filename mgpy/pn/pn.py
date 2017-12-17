from .initialplace import InitialPlace


class PN(object):
    def __init__(self, transitions):
        self.transitions = transitions
        self.__enabled_transitions = [transition for transition in self.transitions if transition.is_enabled()]

    def get_enabled_transitions(self):
        return self.__enabled_transitions

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

    def deposit(self, token, output_places):
        for place in output_places:
            place.deposit(token)
            if place.output_transition.try_enable():
                self.__enabled_transitions.append(place.output_transition)

    def consume_tokens(self, input_places):
        return dict([pair for pair in [place.consume() for place in input_places] if len(pair) == 2])
