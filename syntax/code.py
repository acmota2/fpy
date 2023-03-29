import func

class code:
    def __init__(self, prev_code=None):
        if prev_code:
            self.funcs = prev_code.funcs
        else:
            self.funcs = {}

    def insert_func(self, func: func):
        if func.name not in self.funcs:
            self.funcs[func.name] = {
                'defs': 0,
            }
        self.funcs[func.name]['defs'] += 1
        def_number: int = self.funcs[func.name]['defs']
        # aqui pode dar para verificar se todas têm o mesmo num de args também
        self.funcs[func.name][def_number] = func._arg_list
