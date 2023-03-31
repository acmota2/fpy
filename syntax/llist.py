import syntax.var as var

class llist_term:
    def __init__(
        self,
        type=None,
        *args
    ):
            self.type = type
            match type:
                case 'var':
                    self.content = args[0]
                case 'lister':
                    self.content = {
                        'head': args[0],    # var
                        'tail': args[1]     # llist
                    }
                case 'commas':
                    self.content = {
                        'cont': args[0],
                        'var': args[1]
                    }
                case _:
                    print('Error on llist_term')

    def __eq__(self, other):
        return self.type == other.type and \
            self.content == other.content

class llist_cont:
    def __init__(self, type=None, content=None):
        self.type = type
        match type:
            case 'llist_term':
                self.content = content
            case _:
                print('Error on llist_cont')

    def __eq__(self, other):
        return self.type == other.type \
            and self.content == other.content

class llist:
    def __init__(self, type=None, content: llist_cont=None):
        self.type = type
        match type:
            case 'llist':
                self.content = content
            case _:
                print('Error on llist')

    def __eq__(self, other):
        return self.type == other.type \
            and self.content == other.content
