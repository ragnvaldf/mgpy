from .scheduler import Scheduler


class SimpleScheduler(Scheduler):
    def __init__(self, pn, **kwargs):
        Scheduler.__init__(self, pn, **kwargs)

    def run(self):
        active = self._pn.get_enabled_transitions()

        while len(active) > 0:
            transition_idx = active.pop(0)

            func, params = self._start_firing(transition_idx)
            token = self._run_function(func, params)

            new_enabled = self._complete_firing(transition_idx, token)
            active.extend(new_enabled)

        return self
