class rlist:
    def __init__(self, type=None, rlist_term=None):
        self.type = type
        self.exps = []
        match type:
            case 'rlist':
                if rlist_term:
                    self.exps.extend(rlist_term.exps)
            case _:
                print('Error on rlist')

    def __eq__(self, other):
        return self.type == other.type and \
            self.exps == other.exps

    def add_exp(self, exp):
        self.exps.append(exp)

    def get_ids(self) -> set:
        r: set = {}
        for v in self.exps:
            if v in r:
                return None
            match v.type:
                case 'ID' | 'NUM' | 'STRING' | 'CHAR':
                    r.append(v.var)
                case 'rtuple' | 'rlist':
                    r.extend(v.exps)
        return r
