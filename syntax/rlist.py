class rlist:
    def __init__(self, type=None, content=None):
        self.type = type
        match type:
            case 'rlist':
                self.content = content
            case _:
                print('Error on rlist')

class rlist_cont:
    def __init__(self, type=None, content=None):
        self.type = type
        match type:
            case 'end' | 'rlist_term':
                self.content = content
            case _:
                print('Error on rlist_cont')

class rlist_term:
    def __init__(self, type=None, *args):
            self.type = type
            match type:
                case 'exp':
                    self.content = args[0]
                case 'comma' | 'lister':
                    self.content = {
                        'head': args[0],
                        'tail': args[1]
                    }
                case _:
                    print('Error on rlist_term')
