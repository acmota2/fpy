class eval:
    def __init__(
        self,
        type=None,
        signal=None,
        exp=None,
        eval=None
    ):
        if type == 'eval':
            self.type = type
            self.condition = (signal, exp, eval)
        else:
            print('Error on eval')

    def __eq__(self, other):
        return self.type == other.type and \
            self.conditon == other.conditon
