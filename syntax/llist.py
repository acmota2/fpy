class llist:
    def __init__(self, type=None, content=None):
        self.type = type
        match type:
            case 'llist':
                self.content = content
            case _:
                print('Error on llist')

class llist_cont:
    def __init__(self, type=None, content=None):
        self.type = type
        match type:
            case 'end' | 'llist_term':
                self.content = content
            case _:
                print('Error on llist_cont')

class llist_term:
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
                    print('Error on llist_term')
