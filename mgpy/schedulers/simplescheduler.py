from .scheduler import Scheduler


class SimpleScheduler(Scheduler):
    def __init__(self, pn, **kwargs):
        Scheduler.__init__(self, pn, **kwargs)

    def run(self):
        while self._pn.has_enabled_transitions():
            transition = self._get_enabled_transition()

            input_tokens = self._start_firing(transition)
            token = self._run_function(transition, input_tokens)

            self._complete_firing(transition, token)

        return self
