class ltuple:
    def __init__(self, type=None, ltuple_term=None):
        self.type = type
        self.vars = []
        match type:
            case ' ltuple':
                if ltuple_term:
                    self.vars.extend(ltuple_term.vars)
            case _:
                print('Error on ltuple')

    def __eq__(self, other):
        return self.type == other.type and \
            self.vars == other.vars

    def add_lvar(self, lvar):
        self.vars.append(lvar)

    def get_ids(self):
        r: list = {}
        for v in self.vars:
            match v.type:
                case 'ID':
                    r.append(v.var)
                case 'ltuple' | 'llist':
                    r.extend(v.vars)
        return r
