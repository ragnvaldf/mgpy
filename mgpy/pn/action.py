class Action(object):
    def __init__(self, func, provides, requirements, limit):
        self.__func = func
        self.__provides = provides
        self.__requirements = requirements
        self.__limit = limit

    def get_func(self):
        return self.__func

    def real_func(self):
        return self.__func

    def provides(self, requirement):
        return self.__provides == requirement.provider

    def get_provides(self):
        return self.__provides

    def requirements(self):
        return self.__requirements

    def has_limit(self):
        return self.__limit is not None

    def limit(self):
        return self.__limit
