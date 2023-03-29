class eval:
    def __init__(self, type=None, *args):
        self.type = type
        match type:
            case 'ID' | 'eval':
                self.content = args[0]
            case _:
                self.content = {
                    'eval': args[0],
                    'op': args[1],
                    'aritm': args[2]
                }