class aritm:
    def __init__(self, type=None, op=None, var=None, aritm=None):
        if type == 'aritm':
            self.type = type
            self.aritm = (op, var, aritm)
        else:
            print('Error on aritm')
    
    def __eq__(self, other):
        return self.type == other.type and \
               self.aritm == other.aritm
