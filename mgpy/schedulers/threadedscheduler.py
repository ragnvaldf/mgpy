from .scheduler import Scheduler
from threading import Thread, Condition


class ThreadedScheduler(Scheduler):
    def __init__(self, pn, thread_count=4, **kwargs):
        Scheduler.__init__(self, pn, **kwargs)
        self.__alive = True
        self.__threads = [Thread(group=None, target=self.__run) for _ in range(thread_count)]
        self.__waiting_threads = 0
        self.__cv = Condition()

    def run(self):
        [thread.start() for thread in self.__threads]

        return self

    def join(self):
        [thread.join() for thread in self.__threads]

        return self

    def __run(self):
        while self.__alive:
            with self.__cv:
                if not self._pn.has_enabled_transitions():
                    self.__waiting_threads += 1
                    if self.__waiting_threads == len(self.__threads):
                        self.__alive = False
                        self.__cv.notifyAll()
                        return
                    self.__cv.wait_for(lambda: self._pn.has_enabled_transitions() or not self.__alive)
                    self.__waiting_threads -= 1

                    if not self.__alive:
                        return

                transition = self._get_enabled_transition()
                input_tokens = self._start_firing(transition)

                if self._pn.has_enabled_transitions():
                    self.__cv.notify()

            token = self._run_function(transition, input_tokens)

            with self.__cv:
                self._complete_firing(transition, token)
