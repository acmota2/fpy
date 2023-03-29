class body:
    def __init__(self, type=None, *args):
        self.type = type
        match type:
            case 'exp':
                self.content = args[0]
            case 'statement_body':
                self.content = {
                    'statement': args[0],
                    'body': args[1]
                }
