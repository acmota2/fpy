import type_inference as ti

_string = ti.list_(ti.char_())

class function_info:
    def __init__(self, name='', args=[], type_=ti.Any_(), num_args=1):
        self.name = name
        self.args = args
        self.num_args = num_args
        self.type = type_
        self.errors = []
        self.scope = {}

class code:
    type_aliases = {
        'string': _string
    }

    global_variables = {}

    def __init__(self):
        self.functions = {}
        self.unused = {}

    def del_unused(self, name):
        del self.unused[name]

    def __contains__(self, key):
        return key in self.functions

    def __getitem__(self, key):
        return self.functions[key]
    
    def __setitem__(self, key, value):
        self.functions[key] = value

    def __delitem__(self, key):
        del self.functions[key]

    def add_alias(self, alias_name, equivalence):
        while equivalence in self.type_aliases:
            equivalence = self.type_aliases[equivalence]
        self.type_aliases[alias_name] = equivalence
