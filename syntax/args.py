class args:
    def __init__(self, type=None, content=None):
        self.type = type
        match type:
            case 'lvar':
                self.content = content
                self.ids = content.ids
            case _:
                print('Error on args')

    def __eq__(self, other):
        return self.type == other.type and \
            self.content == other.content
