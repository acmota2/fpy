class singl:
    def __init__(self, type=None, var=None):
        self.type = type
        self.var = var
        match type:
            case 'ID':
                self.compile_time = False
            case _:
                self.compile_time = True
