from .pn import PN
from mgpy.pn.action import Action
from mgpy.pn.transition import Transition, FunctionTransition
from mgpy.pn.place import Place


class MarkedGraph(object):
    def __init__(self, debug=False):
        self.__debug = debug
        self.__actions = []
        self.__transitions = []
        self.__places = []

    def add(self, action):
        assert isinstance(action, Action)
        self.__actions.append(action)

        return self

    def build(self):
        self.__make_places()
        self.__make_arcs()

        for transition in self.__transitions:
            if transition.can_be_enabled():
                transition.enable()

        return PN(self.__transitions)

    def __make_places(self):
        for action in self.__actions:
            nodes = action.get_nodes(self.__find_transition_satisfying)

            for key, value in nodes.items():
                if isinstance(value, Transition):
                    self.__transitions.append(value)

                elif isinstance(value, Place):
                    self.__places.append(value)

                else:
                    assert key == 'required_places'
                    for required_place in value:
                        assert isinstance(required_place, Place)
                        self.__places.append(required_place)

                        if self.__debug:
                            print('Created {} ({})'.format(required_place.__class__.__name__, required_place.name()))
                    continue

                if self.__debug:
                    print('Created {} ({})'.format(value.__class__.__name__, value.name()))

    def __find_transition_satisfying(self, requirement):
        providers = [t for t in self.__transitions
                     if isinstance(t, FunctionTransition) and requirement.satisfied_by(t.product())]
        assert len(providers) == 1, 'Exactly 1 provider must exist for {}'.format(requirement.product)

        return providers[0]

    def __make_arcs(self):
        for place in self.__places:
            place.input_transition().add_output_place(place)
            place.output_transition().add_input_place(place)
