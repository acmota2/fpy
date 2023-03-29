class lambda_:
    def __init__(self, type=None, *args):
        self.type = type
        match type:
            case 'lambda':
                self.content = {
                    'args': args[0],
                    'exp': args[1]
                }
            case _:
                print('Error on lambda')
