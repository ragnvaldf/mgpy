import json


class Scheduler(object):
    def __init__(self, pn, print_all_states_full=False):
        self._pn = pn
        self._print_all_states_full = print_all_states_full

    def _start_firing(self, transition):
        transition.fire()
        func = transition.action.get_func()
        params = self._pn.consume_tokens(transition.input_places())

        self.__print_state_full()

        return func, params

    def _run_function(self, func, params):
        token = func(**params)

        self.__print_state_full()

        return token

    def _complete_firing(self, transition, token):
        transition.disable()
        self._pn.deposit(token, transition.output_places())
        transition.try_enable()

        self.__print_state_full()

    def __print_state_full(self):
        if self._print_all_states_full:
            print(json.dumps(self._pn.get_state_dict(), indent=4))

    def run(self):
        return self
