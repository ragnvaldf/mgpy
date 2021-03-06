class TokenColors(object):
    def __init__(self, colors):
        assert isinstance(colors, list)
        assert len(colors) > 0
        for c in colors:
            assert isinstance(c, tuple) and len(c) == 2 and isinstance(c[0], str)
        self.__colors = colors
        self.__iter_val = 0
        self.__max_iter = len(self.__colors)

    def __iter__(self):
        self.__iter_val = 0

        return self

    def __next__(self):
        if self.__iter_val == self.__max_iter:
            raise StopIteration
        else:
            color = self.__colors[self.__iter_val]
            self.__iter_val += 1

            return color
