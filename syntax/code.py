class code:
    def __init__(self):
        self.funcs = {}
        self.errors = []

    def add_errors(self, errors: list[str]):
        self.errors.extend(errors)

    def insert_func(self, func):
        if func.name not in self.funcs:
            self.funcs[func.name] = {
                'def_num': 0,
                'defs': []
            }
        self.funcs[func.name]['def_num'] += 1
        # aqui pode dar para verificar se todas têm o mesmo num de args também
        self.funcs[func.name]['defs'].append(func)
