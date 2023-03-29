class func_call:
    def __init__(self, type=None, content=None):
        match type:
            case 'func_call':
                self.content = content
            case _:
                print('Error on func_call')

class func_call_cont:
    def __init__(self, type=None, *args):
        self.type = type
        match type:
            case 'RPAR':
                self.content = None
            case 'exp':
                self.content = {
                    'exp': args[0],
                    'func_call_cont': args[1]
                }
