class exp:
    def __init__(self, type=None, content=None):
        self.type = type
        match type:
            case 'rvar' | 'eval' | 'aritm' | 'cond' | 'lambda':
                self.content = content
            case _:
                print('Error on exp')
