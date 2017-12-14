from .pn import PN
from .transition import Transition
from .place import Place
from .initialplace import InitialPlace


class MGBuilder(object):
    def __init__(self):
        self.actions = []

    def add(self, action):
        self.actions.append(action)

        return self

    def build(self):
        transitions = [Transition(action) for action in self.actions]
        for transition in transitions:
            for requirement in transition.action.requirements():
                place = Place(requirement.provider, transition)

                providers = [t for t in transitions if t.action.provides(requirement)]
                assert len(providers) == 1, 'Exactly 1 provider must exist for {}'.format(requirement.provider)
                providers[0].output_places.append(place)

                transition.input_places.append(place)
            if transition.action.has_limit():
                transition.input_places.append(InitialPlace(transition))
            transition.try_enable()

        return PN(transitions)
