from lexer import tokens, literals
import ply.yacc as yacc
from semantics import type_inference as ti
from semantics import errors as err
from semantics import code_ as code

# all
def p_all_first2(p):
    '''
    all : 
        | BEGIN END
    '''
    pass

def p_all_body(p):
    "all : BEGIN body END"
    p[0] = code.code()

# body

def p_body_statement(p):
    "body : statement"
    p[0] = ...

def p_body_statement_list(p):
    "body : body statement"
    p[0] = ...

# statement
def p_statement_function(p):
    "statement : function"
    p[0] = p[1]

def p_statement_alias(p):
    "statement : ALIAS ID '=' typedesc"
    p[0].add_alias(p[2], p[4])

def p_statement_global(p):
    "statement : LET ID annotation '=' conditional"
    if (t := (p[3] & p[5])) and\
        (name1 := (p[2] not in p[0].global_variables)) and\
        (name2 := (p[2] not in p[0])):
        p[0].global_variables[p[2]] = t
    elif not (name1 and name2):
        raise err.name_already_defined()
    else:
        raise err.type_error()

# function
def p_function_nolet(p):
    "function : FDEF prefix args returntype '{' compound '}'"
    if (name := p[2] not in p[0]) and (r := (p[4] & p[6])) and p[3]:
        p[0][p[2]] = ti.function_(
            return_=r,
            args=p[3]
        )
        p[0].cur_f = p[0][p[2]]
    elif not name:
        ti.typeclass.generic = -1
        raise err.name_already_defined()
    else:
        ti.typeclass.generic = -1
        raise err.type_error()
    ti.typeclass.generic = -1


def p_function_let(p):
    "function : FDEF prefix args returntype '{' let_block compound '}'"
    if (name := p[2] not in p[0]) and (r := (p[4] & p[7])) and p[3]:
        p[0][p[2]] = ti.function_(
            return_=r,
            args=p[3]
        )
        p[0].cur_f = p[0][p[2]]
    elif not name:
        ti.typeclass.generic = -1
        raise err.name_already_defined()
    else:
        ti.typeclass.generic = -1
        raise err.type_error()
    ti.typeclass.generic = -1

# args
def p_args_empty(p):
    "args | '(' ')'"
    p[0] = None

def p_args_arg_list(p):
    "args | '(' arg_list ')'"
    p[0] = p[1]

def p_arg_list_one(p):
    "arg_list : lpattern annotation"
    if p[2] and (t := (p[1] & p[2])):
        p[0] = [t]
    else:
        raise err.type_error()

def p_arg_list(p):
    "arg_list : arg_list ',' lpattern annotation"
    if p[4] and (t := (p[3] & p[4])):
        p[0].append(p[4] if p[4] else p[3])
    else:
        raise err.type_error()

def p_prefix(p):
    "prefix : ID"
    p[0] = p[1]

def p_prefix_special(p):
    "prefix : '[' SPECIALID ']'" 
    p[0] = p[2]

def p_returntype(p):
    'returntype : '
    p[0] = ti.Any_()

def p_returntype_exists(p):
    'returntype : RARROW typedesc'
    p[0] = p[2]

# types
def p_annotation(p):
    'annotation : '
    p[0] = ti.Any_()

def p_annotation_exists(p):
    "annotation : ':' typedesc"
    p[0] = p[2]

def p_typedesc(p):
    '''
    typedesc    : typeid
                | typeclass
                | function_type
    '''
    p[0] = p[1]

def p_typedesc_tuple(p):
    "typedesc | '(' tuple_type ')'"
    p[0] = p[2]

def p_typeclass(p):
    "typeclass : TYPECLASS ID"
    match p[1]:
        case 'Num':
            p[0] = ti.Num(p[2])
        case 'Eq':
            p[0] = ti.Eq(p[2])
        case 'Ord':
            p[0] = ti.Ord(p[2])
        case _:
            raise err.class_name_error()

def p_function_type_one(p):
    "function_type : '(' typedesc ')' RARROW typedesc"
    p[0] = ti.function_(return_=p[5], args=[p[2]])

def p_function_type(p):
    "function_type : '(' tuple_type ')' RARROW typedesc"
    p[0] = ti.function_(args=p[2], return_=p[5])

def p_tuple_type_simple(p):
    "tuple_type : typeid ',' typeid"
    p[0] = [p[1], p[3]]

def p_tuple_type_list(p):
    "tuple_type : tuple_type ',' typeid"
    p[0] = p[1].append(p[3])

def p_typeid_int(p):
    "typeid : INT"
    p[0] = ti.int_()

def p_typeid_float(p):
    "typeid : FLOAT"
    p[0] = ti.float_()

def p_typeid_bool(p):
    "typeid : BOOL"
    p[0] = ti.bool_()

def p_typeid_id(p):
    "typeid : ID"
    p[0] = ti.any_()

def p_typeid_list(p):
    "typeid : '[' typedesc ']'"
    p[0] = ti.list_(p[2])

# let_blocks
def p_let_block(p): "let_block : LET '{' let_cond '}'" ; pass
def p_let_cont(p):  "let_cont : assign"                ; pass
def p_let_cont2(p): "let_cont : let_cont ',' assign"   ; pass

def p_assign(p):
    "assign : lpattern annotation '=' conditional"
    if not p[2] & p[4]:
        raise err.type_error()

def p_lpattern(p):
    '''
    lpattern : lvar
             | llist
             | ltuple
    '''
    p[0] = p[1]

def p_llist_empty(p):
    "llist : '[' ']'"
    p[0] = ti.list_()

def p_llist_patterned(p):
    "llist : '[' pattern_list ']'"
    p[0] = p[2]

def p_llist_head_tail(p):
    "llist : '[' lpattern '|' lpattern ']'"
    if p[2] & p[4].content:
        p[0] = p[2]
    else:
        err.type_error()

def p_pattern_list(p):
    "pattern_list : lpattern"
    p[0] = [p[1]]

def p_pattern_list_list(p):
    "pattern_list : pattern_list ',' lpattern"
    if t := (p[1] & p[3]):
        p[0] = t
    else:
        raise err.type_error()
    
def p_ltuple_empty(p):
    "ltuple : '(' ')'"
    p[0] = ti.tuple_()

def p_ltuple(p):
    "ltuple : '(' ltuple_cont ')'"
    p[0] = ti.tuple_(content=p[2])

def p_ltuple_cont(p):
    "ltuple_cont : lpattern ',' lpattern"
    p[0] = [p[1], p[3]]

def p_ltuple_cont1(p):
    "ltuple_cont : ltuple_cont ',' lpattern"
    p[0] = p[1].append(p[3])

def p_lvar(p):
    "lvar : ID"
    p[0] = ti.Any_()

def p_lvar1(p):
    "lvar : '[' SPECIALID ']'"
    p[0] = ti.Any_()

def p_lvar3(p):
    "lvar : INTT"
    p[0] = ti.int_()

def p_lvar4(p):
    "lvar : FLOATT"
    p[0] = ti.float_()

def p_lvar5(p):
    "lvar : CHART"
    p[0] = ti.char_()

def p_lvar6(p):
    "lvar : BOOLT"
    p[0] = ti.bool_()

def p_lvar7(p):
    "lvar : '(' lpattern ')'"
    p[0] = p[2]

# condition
def p_conditional_compound(p):
    "conditional : compound"
    p[0] = p[1]

def p_conditional_ifthenelse(p):
    "conditional : IF conditional THEN conditional ELSE conditional"
    if type(p[2]) == ti.bool_ and (t := (p[4] % p[6])):
        p[0] = t
    else:
        raise err.type_error()

# compound
def p_compound_expression(p):
    "compound : expression"
    p[0] = p[1]

def p_compound_infix(p):
    "compound : compound infix expression"
    type_ = type(p[2])
    if type_ == ti.Any_:
        p[0] = ti.function_(return_=ti.Any_(), content=[p[2] & p[3], p[3] & p[4]])
    elif type_ == ti.function_:
        p[2] = p[2].right_mod(p[3])
        p[0] = p[2] % p[3]
    else:
        err.type_error()  

def p_compound_right_infix(p):
    "compound : '(' compound infix ')'"
    type_ = type(p[1])
    if type_ == ti.Any_:
        p[0] = ti.function_(return_=ti.Any_(), content=[p[2] & p[3], ti.Any_()])
    elif type_ == ti.function_:
        p[0] = p[2] % p[3]
    else:
        err.type_error()

def p_compound_left_infix(p):
    "compound : '(' infix expression ')'"
    type_ = type(p[2])
    if type_ == ti.Any_:
        p[0] = ti.function_(return_=ti.Any_(), content=[ti.Any_(), p[2] & p[3]])
    elif type_ == ti.function_:
        p[0] = p[2].right_mod(p[3])
    else:
        err.type_error()

def p_infix_ID(p):
    "infix : '`' ID '`'"
    if p[2] in parser.function:
        p[0] = parser.code[p[2]]
    else:
        p[0] = ti.Any_()

def p_infix_SPECIALID(p):
    "infix : SPECIALID"
    if p[1] in parser.code:
        p[0] = parser.code[p[1]]
    else:
        p[0] = ti.Any_()

#expression
def p_expression(p):
    '''
    expression  : multivar
                | lambda
                | cond_block
    '''
    p[0] = p[1]

#cond_block
def p_cond_block(p):
    "cond_block : COND '{' cond ',' ELSE ':' conditional '}'"
    p[0] = p[3] & p[7]

def p_cond(p):
    "cond : cond_singl"
    p[0] = p[1]

def p_cond(p):
    "cond : cond ',' cond_singl"
    try:
        p[0] &= p[1] & p[2]
    except:
        raise err.type_error()

def p_cond_singl(p):
    "cond_singl : conditional ':' conditional"
    if type(p[1]) != ti.bool_:
        raise err.type_error()
    p[0] = p[3]

#lambda
def p_lambda_no_args(p):
    "lambda : FDEF '(' ')' '{' conditional '}'"
    p[0] = p[5]

def p_lambda_args(p):
    "lambda : FDEF '(' pattern_list ')' '{' conditional '}'"
    p[0] = ti.function_(return_=p[6], args=p[3])

#multivar
def p_primaryvar(p):
    """
    multivar    : primaryvar
                | rlist
                | rtuple
    """
    p[0] = p[1]

def p_multivar_call(p):
    "multivar : multivar '(' condition_list ')'"
    _type = type(p[1])
    if p[1] in parser.code:
        parser.check_args = parser.code[p[1]].type.check_args()
        p[1] = ...
        parser.check_args = None

    else:
        raise err.type_error()

#primaryvar
def p_primaryvar_ID(p):
    "primaryvar : ID"
    p[0] = ti.Any_()

def p_primaryvar_SPECIALID(p):
    "primaryvar : SPECIALID"
    p[0] = ti.Any_()

def p_primaryvar_int(p):
    "primaryvar : INTT"
    p[0] = ti.int_()

def primaryvar_string(p):
    "primaryvar : STRINGT"
    p[0] = ti.list_(content=ti.char_())

def p_primaryvar_float(p):
    "primaryvar : FLOATT"
    p[0] = ti.float_()

def p_primaryvar_char(p):
    "primaryvar : CHART"
    p[0] = ti.char_()

def p_primaryvar_bool(p):
    "primaryvar : BOOLT"
    p[0] = ti.bool_()

def p_primaryvar_conditional(p):
    "primaryvar : '(' conditional ')'"
    p[0] = p[2]

#rtuple
def p_rtuple_empty(p):
    "rtuple : '(' ')'"
    p[0] = ti.tuple_()

def p_rtuple_cont(p):
    "rtuple : '(' rtuple_cont ')'"
    p[0] = p[2]

def p_rtuple_cont_2_case(p):
    "rtuple : conditional ',' conditional"
    p[0] = p[1] & p[2]

def p_rtuple_cont_rest_case(p):
    "rtuple_cont : rtuple_cont ',' conditional"
    p[0] &= p[1] & p[2]

# rlist
def p_rlist_empty(p):
    "rlist : '[' ']"
    p[0] = ti.list_()

def p_rlist_normal(p):
    "rlist : '[' condition_list ']'"
    p[0] = ti.list_(content=p[2])

def p_rlist_condition_list(p):
    "rlist : '[' conditional '|' conditional ']'"
    if type(p[2]) == type(p[4].content):
        p[0] = ti.list_(p[2])
    else:
        raise err.type_error()

def p_rlist_ranger(p):
    "rlist : '[' conditional RANGER conditional ']'"
    if isinstance(p[2], ti.int_) and isinstance(p[4], ti.int_):
        p[0] = ti.list_(content=ti.int_())
    else:
        raise err.type_error()

def p_rlist_condition_list_conditional(p):
    "condition_list : conditional"
    if parser.check_args:
        p[0] = [p[1] & next(parser.check_args)]
    else:
        p[0] &= p[1]

def p_rlist_condition_list_list(p):
    "condition_list : condition_list ',' conditional"
    if not p[2]:
        raise err.type_error()
    if parser.check_args:
        p[0].append(p[1] & next(parser.check_args))
    else:
        try:
            p[0] &= p[1] & p[2]
        except:
            raise err.type_error()

def p_error(p):
    if not p:
        pass
    print(f"Parse error on '{err.red_bold}{p.value}' at {p.lineno(0)}")

parser = yacc.yacc()
parser.code: code.code = code.code()
