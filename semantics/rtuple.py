class ltuple:
    def __init__(self, type=None, rtuple_term=None):
        self.type = type
        self.exps = []
        match type:
            case 'rtuple':
                if rtuple_term:
                    self.exps.extend(rtuple_term.exps)
            case _:
                print('Error on rtuple')

    def __eq__(self, other):
        return self.type == other.type and \
            self.exps == other.exps

    def add_exp(self, exp):
        self.exps.append(exp)

    def get_ids(self) -> set:
        r: set = {}
        for v in self.exps:
            match v.type:
                case 'ID' | 'NUM' | 'STRING' | 'CHAR':
                    r.append(v.var)
                case 'rtuple' | 'rlist':
                    r.extend(v.exps)
        return r
