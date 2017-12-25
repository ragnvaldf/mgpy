import json


class Scheduler(object):
    def __init__(self, pn, print_full_state_on_change=False, print_state_changes=False):
        self._pn = pn
        self.__print_full_state_on_change = print_full_state_on_change
        self.__print_state_changes = print_state_changes
        self.__enabled_transitions = self._pn.get_enabled_transitions()

    def run(self):
        return self

    def _get_enabled_transition(self):
        return self.__enabled_transitions[0]

    def _start_firing(self, transition):
        input_tokens = self._pn.fire(transition)

        self.__print_full_state()
        if self.__print_state_changes:
            print('{}: Fire!'.format(transition.name()))

        return input_tokens

    def _complete_firing(self, transition, token):
        self._pn.deposit_token_in_output_places(token, transition)
        if transition.can_be_enabled():
            self._pn.enable(transition)
        else:
            self._pn.disable(transition)

        self.__print_full_state()
        if self.__print_state_changes:
            print('{}: Done!'.format(transition.name()))

    def __print_full_state(self):
        if self.__print_full_state_on_change:
            print(json.dumps(self._pn.get_state_dict(), indent=4))
