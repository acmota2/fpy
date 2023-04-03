class cond:
    def __init__(self, type=None):
        if type == 'cond':
            self.type = type
            self.conditions = []
        else:
            print('Error on cond')

    def add_condition(self, evalexp):
        self.conditions.append(evalexp)


class if_then_else:
    def __init__(self, type=None, eval=None, then=None, else_=None):
        self.eval = eval
        self.then = then
        self.else_ = else_

    def __eq__(self, other):
        return self.eval == other.eval and \
            self.then == other.then and \
            self.else_ == other.else_
