from ..pn.pn import PN


class PNBuilder(object):
    def __init__(self):
        self.actions = []

    def add(self, action):
        self.actions.append(action)

        return self

    def build(self):
        pn = PN(self.actions)
        pn.build()
        pn.refresh_transition_states()

        return pn
