import json


class Scheduler(object):
    def __init__(self, pn, print_all_states_full=False):
        self._pn = pn
        self._print_all_states_full = print_all_states_full

    def _start_firing(self, transition):
        func, params = self._pn.start_firing(transition)

        if self._print_all_states_full:
            self.__print_state_full()

        return func, params

    def _run_function(self, func, params):
        token = func(**params)

        if self._print_all_states_full:
            self.__print_state_full()

        return token

    def _complete_firing(self, transition, token):
        new_enabled = self._pn.complete_firing(transition, token)

        if self._print_all_states_full:
            self.__print_state_full()

        return new_enabled

    def __print_state_full(self):
        print(json.dumps(self._pn.get_state_dict(), indent=4))

    def run(self):
        return self
