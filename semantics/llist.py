class llist:
    def __init__(self, type=None, llist_term=None):
        self.type = type
        self.vars = []
        match type:
            case 'llist':
                if llist_term:
                    self.vars.extend(llist_term.vars)
            case _:
                print('Error on llist')

    def __eq__(self, other):
        return self.type == other.type and \
            self.vars == other.vars
    
    def add_lvar(self, lvar):
        self.vars.append(lvar)

    def get_ids(self) -> set:
        r: list = {}
        for v in self.vars:
            if v in r:
                return None
            match v.type:
                case 'ID':
                    r.append(v.var)
                case 'ltuple' | 'llist':
                    r.extend(v.vars)
        return r
