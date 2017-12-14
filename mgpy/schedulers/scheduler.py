import json
from ..pn import start_firing, complete_firing


class Scheduler(object):
    def __init__(self, pn, print_all_states_full=False):
        self._pn = pn
        self._print_all_states_full = print_all_states_full

    def _start_firing(self, transition):
        func, params = start_firing(transition)

        self.__print_state_full()

        return func, params

    def _run_function(self, func, params):
        token = func(**params)

        self.__print_state_full()

        return token

    def _complete_firing(self, transition, token):
        new_enabled = complete_firing(transition, token)

        self.__print_state_full()

        return new_enabled

    def __print_state_full(self):
        if self._print_all_states_full:
            print(json.dumps(self._pn.get_state_dict(), indent=4))

    def run(self):
        return self
