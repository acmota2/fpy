class body:
    def __init__(self, type=None, content=None):
        if type != 'body':
            print('Error on body')
        else:
            self.type = type
            self.statements = {content}
