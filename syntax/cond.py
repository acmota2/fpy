class cond:
    '''Classe definida por dicionários. Aceita os tipos
    if_else
    if_then_else
e guarda o conteúdo das regras de cond:
    COND LBRACE condition RBRACE
    IF eval THEN exp ELSE exp
da gramática'''

    def __init__(self, type=None, *args):
        self.type = type
        match type:
            case 'if_else':
                self.content = args[0]
            case 'if_then_else':
                self.content = {
                    'eval': args[0],
                    'then': args[1],
                    'else': args[2]
                }
            case _:
                print('Error on cond')

class condition:
    def __init__(self, type=None, cont=None, exp=None):
        self.type = type
        match type:
            case 'condition':
                self.content = {
                    'cont': condition_cont,
                    'exp': exp
                }
            case _:
                print('Error on condition')

class condition_cont:
    def __init__(self, type=None, *args):
        self.type = type
        match type:
            case 'evalexp':
                self.content = args[0]
            case 'evalexp_cont':
                self.content = {
                    'evalexp': args[0],
                    'cont': args[1]
                }
            case _:
                print('Error on condition_cont')

class evalexp:
    def __init__(self, type=None, exp=None):
        self.type = type
        match type:
            case 'evalexp':
                self.content = exp
            case _:
                print('Error on evalexp')
