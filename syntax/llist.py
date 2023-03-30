import singl

class llist_term:
    def __init__(self, type=None, singl: singl=None, head: singl=None, tail=None):
            self.type = type
            match type:
                case 'singl':
                    self.content = singl
                case 'comma' | 'lister':
                    self.content = {
                        'head': head,    # singl
                        'tail': tail     # llist
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
            case 'end' | 'llist_term':
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
