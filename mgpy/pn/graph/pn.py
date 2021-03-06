class PN(object):
    def __init__(self, transitions):
        self.__transitions = transitions
        self.__enabled_transitions = list(filter(lambda transition: transition.is_enabled(), self.__transitions))

    def get_enabled_transitions(self):
        return self.__enabled_transitions

    def get_state_dict(self):
        d = {}
        for transition in self.__transitions:
            d[transition.name()] = {}
            d[transition.name()]['State'] = str(transition.state())
            for place in transition.input_places():
                d[transition.name()][place.name()] = place.token_count()

        return d

    def has_enabled_transitions(self):
        return len(self.__enabled_transitions) > 0

    def fire(self, transition):
        self.__enabled_transitions.remove(transition)
        transition.fire()

        return self.consume_tokens(transition.input_places())

    def enable(self, transition):
        transition.enable()
        self.__enabled_transitions.append(transition)

    def disable(self, transition):
        transition.disable()

    def deposit_token_in_output_places(self, token, transition):
        self.deposit(token, transition.output_places())

    def deposit(self, token, output_places):
        for place in output_places:
            place.deposit(token)
            if place.output_transition().can_be_enabled():
                self.enable(place.output_transition())

    def consume_tokens(self, input_places):
        return [place.consume() for place in input_places]
