from .typeinference import *
from .variable_handler import *
from errors import *
from enum import Enum
from re import compile

arg_conflict = Enum("arg_check", ["type_conflict", "less_generic", "redefinition", "no_conflict"])

class function_info:
    ID_matcher = compile(r'[_a-zA-Z]\w*')
    
    def __init__(self, name="", type_=Any_(), line=0, reserved=False):
        self.name: str = name
        self.line: int = line
        self.type: function_ = type_
        self.scope: dict = {}
        self.args: list = []
        self.reserved = reserved

    def __str__(self):
        return f"{self.name}: {self.type}"

    def __repr__(self):
        return str(self)
    
    def search_in_args(self, name):
        for arg in self.args:
            if name in arg:
                return arg[name]

    def recheck_type(self, other):
        self.type &= other.type

    def arg_checker(self, f: function_) -> arg_conflict:
        r = arg_conflict.no_conflict
        if not self.type or  not f or len(self.type.args) != len(f.args):
            return arg_conflict.redefinition

        for arg1, arg2 in zip(self.type.args, f.args):
            type_ = arg1 & arg2
            type_arg2 = type(arg2)
            if type_arg2 == composite and arg2.empty:
                r = arg_conflict.less_generic
            elif not type_:
                return arg_conflict.redefinition
        return r

    def scope_check(self, name) -> bool:
        return name in self.scope

    def scope_in_error(self, arg: arg_scope):
        for v in arg.names.values():
            if v.name in self.scope:
                return self.scope[v.name]
            if v.name != '_' and self.ID_matcher.match(v.name):
                self.scope[v.name] = v
        return None
    
    def update_return(self, new_return: variable):
        if t := (self.type.return_ & new_return.type):
            self.type.return_ = t
            return True
        return False

class code_:
    type_aliases = {}
    not_found_aliases = set()
    global_variables = {}
    functions: dict[function_info] = {}
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

    def update_function_definition(self, name: str, type_args, return_):
        f_type = (
            return_ if type_args == [] else function_(args=type_args, return_=return_)
        )
        if name in self.global_variables:
            return (arg_conflict.redefinition, f_type)
        f: function_info = self.functions[name]
        f.type = f_type & f.type
        return (f.arg_checker(f_type), f_type)

    def new_function_definition(self, name: str, line: int):
        f: function_info = None
        if name in self.not_yet_found:
            f = self.not_yet_found[name]
            del self.not_yet_found[name]
            self.functions[name] = function_info(name=f.name, type_=f.type, line=line)
        elif name not in self.functions:
            f = function_info(name=name, type_=Any_(), line=line)
            self.functions[name] = f

    def lvar_in_scope(self, name: str):
        if name in self.functions[self.cur_f].scope:
            return self.functions[self.cur_f].scope[name]
        return None

    def deal_with_name(self, name: str):
        if not self.cur_f:
            return Any_()
        if name in self.functions:
            return self.functions[name].type
        elif name in self.global_variables:
            return self.global_variables[name].type
        elif name in self.functions[self.cur_f].scope:
            return self.functions[self.cur_f].scope[name].type
        return Any_()

    def add_alias(self, alias_name, equivalence):
        equivalence = self.add_alias_rec(equivalence)
        self.type_aliases[alias_name] = equivalence
        return True

    def add_alias_rec(self, equivalence):
        match equivalence:
            case function_():
                for arg in equivalence.args:
                    arg = self.add_alias_rec(arg)
                equivalence.return_ = self.add_alias_rec(equivalence.return_)
                return equivalence
            case tuple_():
                for arg in equivalence.content:
                    arg = self.add_alias_rec(arg)
                return equivalence
            case list_():
                equivalence.content = self.add_alias_rec(equivalence.content)
                return equivalence
            case Any_():
                return self.check_single_alias(equivalence)

    def check_single_alias(self, equivalence: Any_):
        if issubclass(type(equivalence), Any_):
            return equivalence
        if equivalence.name in self.not_found_aliases:
            return None
        while equivalence.name in self.type_aliases:
            equivalence = self.type_aliases[equivalence.name]
        return equivalence

    def check_alias(self, type_id):
        if type_id in self.type_aliases:
            return self.type_aliases[type_id]
        self.not_found_aliases.add(type_id)
        return Any_(name=type_id)

    def func_body_id(self, name, line):
        if name in self.functions:
            f: function_info = self.functions[name]
            return var_function(name=name, type_=f.type, line=line)
        if name in self.global_variables:
            return self.global_variables[name]
        if self.cur_f and (name in self.functions[self.cur_f].scope):
            return self.functions[self.cur_f].scope[name]
        r = variable(name=name, type_=Any_(), line=line)
        self.not_yet_found[name] = r
        return r

    def update_variable_type(self, var: variable) -> list[bool | Any_]:
        t = None
        v = None
        if not var:
            return [None]
        if not self.cur_f:
            return [True]
        if not var.is_id:
            return [True] # como se nada fosse
        if var.name in self.functions[self.cur_f].scope and (t := (var.type & (v := self.functions[self.cur_f].scope[var.name]).type)):
            self.functions[self.cur_f].scope[var.name].type = t
            return [True]
        if var.name in self.not_yet_found and (t := (var.type & (v := self.not_yet_found[var.name]).type)):
            self.not_yet_found[var.name].type = t
            return [True]
        if var.name in self.functions and (t := (var.type & (v := self.functions[var.name]).type)):
            self.functions[var.name].type = t
            return [True]
        if var.name in self.global_variables and (t := (var.type & (v := self.global_variables[var.name]).type)):
            self.global_variables[var.name].type = t
            return [True]
        return [False, v]
