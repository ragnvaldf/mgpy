from ..pn.mg import MarkedGraph
from ..pn.pn import PN


class PNBuilder(object):
    def __init__(self):
        self.actions = []

    def add(self, action):
        self.actions.append(action)

        return self

    def build(self):
        mg = MarkedGraph(self.actions)
        mg.build()

        return PN(mg)
