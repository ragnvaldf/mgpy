import json


class Scheduler(object):
    def __init__(self, pn, print_all_states_full=False):
        self._pn = pn
        self._print_all_states_full = print_all_states_full
        self.__enabled_transitions = self._pn.get_enabled_transitions()

    def run(self):
        return self

    def _get_enabled_transition(self):
        return self.__enabled_transitions[0]

    def _start_firing(self, transition):
        input_tokens = self._pn.fire(transition)

        self.__print_state_full()

        return input_tokens

    def _run_function(self, transition, input_tokens):
        token = transition.action.get_func()(**argument_dict_from_tokens(input_tokens))

        self.__print_state_full()

        return token

    def _complete_firing(self, transition, token):
        self._pn.deposit_token_in_output_places(token, transition)
        if transition.can_be_enabled():
            self._pn.enable(transition)
        else:
            self._pn.disable(transition)

        self.__print_state_full()

    def __print_state_full(self):
        if self._print_all_states_full:
            print(json.dumps(self._pn.get_state_dict(), indent=4))


def argument_dict_from_tokens(tokens):
    return dict([pair for pair in tokens if len(pair) == 2])
