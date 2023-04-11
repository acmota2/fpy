class statement:
    def __init__(self, type=None, var=None, exp=None):
        if type in ['assign', 'reassign']:
            self.type = type
            self.var = var
            self.exp = exp
        else:
            print('Error on statement')
