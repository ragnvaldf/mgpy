from .pn import PN
from .functiontransition import FunctionTransition
from .place import Place
from .initialplace import InitialPlace


class MGBuilder(object):
    def __init__(self):
        self.__actions = []
        self.__transitions = []
        self.__places = []

    def add(self, action):
        self.__actions.append(action)

        return self

    def build(self):
        self.__make_transitions()
        self.__make_places()
        self.__make_arcs()

        for transition in self.__transitions:
            if transition.can_be_enabled():
                transition.enable()

        return PN(self.__transitions)

    def __make_transitions(self):
        self.__transitions = [FunctionTransition(action.product(), action.get_func()) for action in self.__actions]

    def __make_places(self):
        for transition, action in zip(self.__transitions, self.__actions):
            if action.has_limit():
                self.__places.append(InitialPlace(transition, action.limit()))

            for requirement in action.requirements():
                providers = [t for t, a in zip(self.__transitions, self.__actions) if a.provides(requirement)]
                assert len(providers) == 1, 'Exactly 1 provider must exist for {}'.format(requirement.product)

                self.__places.append(Place(requirement.product, providers[0], transition))

    def __make_arcs(self):
        for place in self.__places:
            if place.input_transition is not None:
                place.input_transition.add_output_place(place)
            if place.output_transition is not None:
                place.output_transition.add_input_place(place)
