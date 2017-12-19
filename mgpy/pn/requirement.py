class Requirement(object):
    def __init__(self, product):
        self.product = product

    def satisfied_by(self, product):
        return self.product == product
