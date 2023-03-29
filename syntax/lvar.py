class lvar:
    def __init__(self, type=None, content=None):
        self.type = type
        match type:
            case 'singl' | 'llist' | 'lltuple':
                self.content = content
            case _:
                print('Error on lvar')
