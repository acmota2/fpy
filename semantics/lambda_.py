class lambda_:
    def __init__(self, type=None, args=None, exp=None):
        if type == 'lambda':
            self.type = type
            self.args = args
            self.exp = exp
        else:
            print('Error on lambda')

    def __eq__(self, other):
        return self.type == other.type and \
               self.args == other.args and \
               self.exp == other.exp
