import type_inference as ti

_string = ti.list_(ti.char_())

class function_info:
    def __init__(self, name='', args=[], type_=ti.Any_(), num_args=1, lines=()):
        self.name = name
        self.args = args
        self.num_args = num_args
        self.type = type_
        self.errors = []
        self.scope = {}
        self.lines = lines

    def __str__(self):
        return self.type
    
    def __repr__(self):
        return str(self)

class not_yet_found:
    def __init__(self, line_info, line, type):
        self.line_info = line_info
        self.line = line
        self.type = type


class code_:
    type_aliases = {
        'string': _string
    }
    global_variables = {}
    functions = {}
    not_yet_found = {}
    cur_f: function_info = None

    def __init__(self):
        pass

    def del_when_found(self, name):
        del self.not_yet_found[name]

    def __contains__(self, key):
        return key in self.functions

    def __getitem__(self, key):
        return self.functions[key]
    
    def __setitem__(self, key, value):
        self.functions[key] = value

    def __delitem__(self, key):
        del self.functions[key]

    def deal_with_name(self, name: str):
        if name in self.functions:
            return self.functions[name]
        elif name in self.global_variables:
            return self.global_variables[name]
        elif name in self.cur_f.scope:
            return self.cur_f.scope[name]
        return ti.Any_()

    def add_alias(self, alias_name, equivalence):
        while equivalence in self.type_aliases:
            equivalence = self.type_aliases[equivalence]
        self.type_aliases[alias_name] = equivalence
