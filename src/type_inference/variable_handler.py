from .typeinference import *
from collections import OrderedDict

class variable:
    def __init__(self, name=None, type_=Any_(), line=0, is_id=True):
        self.name = name
        self.line = line
        self.type = type_
        self.is_id = is_id
    
    # para debug
    def __repr__(self):
        return f"variable {(self.name, self.line, self.type)}"

    def promote(self, args):
        match self.type:
            case singleton() | composite() | Num() | Eq() | Ord():
                return None
            case Any_():
                return var_function(name=self.name, line=self.line, type_=function_(args=[x.type for x in args], return_=Any_()))

class var_function(variable):
    def __init__(self, name=None, type_: function_=Any_(), line=0, is_id=True):
        self.name = name
        self.line = line
        self.type = type_
        self.is_id = is_id
    
    # para debug
    def __repr__(self):
        return f"function {(self.name, self.line, self.type)}"
    
    def promote(self, args):
        return self
    
    def verify_args(self, args):
        num_args: int = 0
        if (num_args := len(self.type.args)) != len(args):
            return (
                False,
                self,
                function_(args=args, return_=self.type.return_)
            )
        for i in range(num_args):
            tmp = self.type.args[i] & args[i].type
            if not tmp:
                return (False, tmp, args[i].type)
            self.type.args[i] = tmp
        print(self)
        return (True, None, None)

    def modulo(self, args):
        for i in range(len(args)):
            print(self.type)
            self.type = self.type % args[i].type
        self.is_id = False
        if self.name == 'not':
            print("EU SOU O NOT!", isinstance(self.type, function_))
        r = self if isinstance(self.type, function_) else variable(
            name=self.name, type_=self.type, line=self.line, is_id=False
        )
        return r

class arg_scope:
    def __init__(self):
        self.names = OrderedDict() # mega pedantic...
        # formato de entrada: variable

    def update_types(self, t: Any_):
        to_compare = flatmap_type(t)
        for k, typ in zip(self.names.keys(), to_compare):
            # again, sendo pedantic
            self.names[k].type &= typ

    def __str__(self):
        return str(self.names)
    
    def __repr__(self):
        return str(self)

    def __contains__(self, key):
        return key in self.names

    def __getitem__(self, key):
        return self.names[key]

    def __setitem__(self, key, value):
        self.names[key] = value

    def __delitem__(self, key):
        del self.names[key]

def left_infix_checker(op: var_function, operand: variable):
    operand_new_type = op.type.args[0] & operand.type
    if v := (op.type % operand.type):
        op.type = v
        op.is_id = False
        return op, operand_new_type
    return None, None

def right_infix_checker(op: var_function, operand: variable):
    operand_new_type = op.type.args[1] & operand.type
    if v := (op.type.right_mod(operand.type)):
        op.type = v
        op.is_id = False
        return op, operand_new_type
    return None, None

def infix_checker(operand1: variable, op: var_function, operand2: variable):
    operand1_new_type = op.type.args[0] & operand1.type
    operand2_new_type = op.type.args[1] & operand2.type
    if (v := (op.type.right_mod(operand2_new_type))) and operand2_new_type and operand1_new_type and v:
        v %= operand1_new_type
        op.type = v
        op.is_id = False
        return op, operand1_new_type, operand2_new_type
    return None, None, None

def make_htlist(var1: variable, var2: variable, line: int) -> variable:
    return variable(type_=htlist_(content=var1.type, tail=var2.type, is_empty=False), line=line, is_id=False)

def make_discrete_list(content: list[Any_], line: int) -> variable:
    return variable(type_=discrete_list(content=[x.type for x in content], is_empty=False), line=line, is_id=False)

def make_tuple(content: list[Any_], line: int) -> variable:
    return variable(type_=tuple_(content=[x.type for x in content], is_empty=False), line=line, is_id=False)