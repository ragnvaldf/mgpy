from .scheduler import Scheduler


class SimpleScheduler(Scheduler):
    def __init__(self, pn, **kwargs):
        Scheduler.__init__(self, pn, **kwargs)

    def run(self):
        active = self._pn.get_enabled_transitions()

        while len(active) > 0:
            transition = active.pop(0)

            func, params = self._start_firing(transition)
            token = self._run_function(func, params)

            self._complete_firing(transition, token)

        return self
