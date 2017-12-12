from .scheduler import Scheduler
from threading import Thread, Condition


class ThreadedScheduler(Scheduler):
    def __init__(self, pn, thread_count, **kwargs):
        Scheduler.__init__(self, pn, **kwargs)
        self.alive = True
        self.threads = [Thread(group=None, target=self.__run) for _ in range(thread_count)]
        self.waiting_threads = 0
        self.enabled_transitions = self._pn.get_enabled_transitions()
        self.cv = Condition()

    def run(self):
        [thread.start() for thread in self.threads]

        return self

    def join(self):
        [thread.join() for thread in self.threads]

        return self

    def __run(self):
        while self.alive:
            with self.cv:
                if len(self.enabled_transitions) == 0:
                    self.waiting_threads += 1
                    if self.waiting_threads == len(self.threads):
                        self.alive = False
                        self.cv.notifyAll()
                        return
                    self.cv.wait_for(lambda: len(self.enabled_transitions) > 0 or not self.alive)
                    self.waiting_threads -= 1

                    if not self.alive:
                        return

                transition_idx = self.enabled_transitions.pop(0)
                func, params = self._start_firing(transition_idx)

                if len(self.enabled_transitions) > 0:
                    self.cv.notify()

            token = self._run_function(func, params)

            with self.cv:
                new_enabled = self._complete_firing(transition_idx, token)
                self.enabled_transitions.extend(new_enabled)
