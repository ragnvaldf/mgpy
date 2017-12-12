class PreCondition(object):
    def __init__(self, name):
        self.name = name


class SimplePreCondition(PreCondition):
    def __init__(self, func, name):
        PreCondition.__init__(self, name)
        self.func = func


class SiphonPreCondition(PreCondition):
    siphon_counter = 0

    def __init__(self, token_count):
        SiphonPreCondition.siphon_counter += 1
        PreCondition.__init__(self, 'Siphon{}-{}'.format(SiphonPreCondition.siphon_counter, token_count))
        self.token_count = token_count
