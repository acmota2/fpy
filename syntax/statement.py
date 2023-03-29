class statement:
    def __init__(self, type=None, content=None):
        match type:
            case 'assign' | 'reassing':
                self.content = content
            case _:
                print('Error on statement')

class reassing_assign:
    def __init__(self, type=None, *args):
        match type:
            case 'assign' | 'reassign':
                self.content = {
                    'lvar': args[0],
                    'exp': args[1]
                }
            case _:
                print(f'Error on {self.type}')
