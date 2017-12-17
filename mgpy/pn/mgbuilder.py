from .pn import PN
from .functiontransition import FunctionTransition
from .place import Place
from .initialplace import InitialPlace


class MGBuilder(object):
    def __init__(self):
        self.actions = []

    def add(self, action):
        self.actions.append(action)

        return self

    def build(self):
        transitions = [action.to_transition() for action in self.actions]
        for transition in transitions:
            for requirement in transition.action.requirements():
                place = Place(requirement.provider, transition)

                providers = [t for t in transitions if t.action.provides(requirement)]
                assert len(providers) == 1, 'Exactly 1 provider must exist for {}'.format(requirement.provider)
                providers[0].add_output_place(place)

                transition.add_input_place(place)
            if transition.action.has_limit():
                transition.add_input_place(InitialPlace(transition))
            transition.try_enable()

        return PN(transitions)
