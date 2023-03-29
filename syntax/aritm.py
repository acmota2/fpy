class aritm:
    def __init__(self, type=None, *args):
        self.type = type
        match type:
            case 'ID' | 'NUM' | 'aritm':
                self.content = args[0]
            case _:
                self.content = {
                    'lval': args[0],
                    'op':   args[1],
                    'rval': args[2]
                }
