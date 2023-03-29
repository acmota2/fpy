class rtuple:
    def __init__(self, type=None, *args):
        self.type = type
        match type:
            case 'LPAR':
                self.content = None
            case 'cont':
                self.content = {
                    'rtuple_cont': args[0],
                    'exp': args[1]
                }
            case _:
                print('Error on rtuple')

class rtuple_cont:
    def __init__(self, type=None, *args):
        self.type = type
        match type:
            case 'exp':
                self.content = args[0]
            case 'cont':
                self.content = {
                    'rtuple_cont': args[0],
                    'exp': args[1]
                }
