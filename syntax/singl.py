class singl:
    def __init__(self, type=None, var=None):
        self.type = type
        self.var = var
        match type:
            case 'ID':
                self.compile_time = False
                self.ids = {var}
            case _:
                self.compile_time = True
                self.ids = {}

    def __eq__(self, other):
        return self.type == self.type \
            and self.var == self.var
