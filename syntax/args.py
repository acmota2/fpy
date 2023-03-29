class args:
    def __init__(self, type=None, content=None):
        self.type = type
        match type:
            case 'lvar':
                self.content = content
            case _:
                print('Error on args')
