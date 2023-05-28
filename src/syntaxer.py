from lexer import tokens, literals, lexer
import ply.yacc as yacc
import errors as err
import type_inference as ti
import sys
from functools import reduce

# all
def p_all_first2(p):
    """all :
           | BEGIN END
    """
    pass

def p_all_body(p):
    "all : BEGIN body END"
    for v in parser.code.not_yet_found.values():
        err.variable_not_in_scope(v.name, v.line)

# body
def p_body_statement(p):
    "body : statement"
    pass

def p_body_statement_list(p):
    "body : body statement"
    pass

# statement
def p_statement_function(p):
    "statement : function"
    p[0] = p[1]

def p_statement_alias(p):
    "statement : ALIAS ID '=' typedesc"
    print("ALIAS", p[2], p[4], type(p[4]))
    parser.code.add_alias(p[2], p[4])

def p_statement_global(p):
    "statement : LET ID annotation '=' conditional"
    name1 = p[2] not in parser.code.global_variables
    name2 = p[2] not in parser.code
    if v := parser.code.not_yet_found.get(p[2], None):
        if not v.type & p[3] & p[5].type:
            parser.err_type = err.err_types.type
            err.fpy_type_error(v.name, v.type, p[5].type, p.lexer.lineno)
            p_error(p)
        parser.code.del_when_found(v.name)
    if (t := (p[3] & p[5].type)) and name1 and name2:
        parser.code.global_variables[p[2]] = ti.variable(p[2], t, p.lexer.lineno)
    elif not (name1 and name2):
        parser.err_type = err.err_types.name
        err.name_already_defined(
            p[2],
            p.lexer.lineno,
            parser.code[p[2]].line
            if name1
            else parser.code.global_variables[p[2]].line,
        )
        p_error(p)
    else:
        parser.err_type = err.err_types.name
        err.fpy_type_error(p[2], p[3], p[5], p.lexer.lineno)
        p_error(p)

def p_function(p):
    "function : scope conditional '}'"
    old_type = parser.code[parser.code.cur_f].type.return_
    if not parser.code[parser.code.cur_f].update_return(p[2]):
        parser.err_type = err.err_types.type
        err.fpy_type_error(p[2].name, old_type, p[2].type, p[2].line)
        p_error(p)
    for var in parser.code[parser.code.cur_f].scope.values():
        if (
            var.name != parser.code.cur_f
            and var.name not in parser.code[parser.code.cur_f].scope
        ):
            err.variable_not_in_scope(var.name, p.lexer.lineno)
            parser.err_type = err.err_types.scope
            p_error(p)
    parser.code[parser.code.cur_f].scope = {}
    parser.code.cur_f = ''
    ti.reset_generics()

def p_scope(p):
    """
    scope : main_scope
          | main_scope let_block
    """
    p[0] = p[1]

def p_main_scope(p):
    "main_scope : new_f args returntype '{'"
    t = parser.code.update_function_definition(p[1], p[2], p[3])
    match t[0]:
        case ti.arg_conflict.less_generic:
            err.argument_warning(p[3], p[2])
        case ti.arg_conflict.redefinition:
            f = parser.code[p[1]]
            err.name_already_defined(p[1], p.lexer.lineno, f.line)
            parser.err_type = err.err_types.name
            p_error(p)
        case ti.arg_conflict.type_conflict:
            parser.err_type = err.err_types.type
            err.fpy_type_error(p[1], p[3], t[1], p.lexer.lineno)
            p_error(p)
        case ti.arg_conflict.no_conflict:
            p[0] = t[1]

def p_lvar_scope(p):
    "new_f : FDEF prefix"
    parser.code.new_function_definition(p[2], p.lexer.lineno)
    parser.code.cur_f = p[2]
    p[0] = p[2]

# args
def p_args_empty(p):
    "args : '(' ')'"
    p[0] = []

def p_args_arg_list(p):
    "args : '(' arg_list ')'"
    p[0] = p[2]

def p_lpattern_scope(p):
    "lpattern_scope :"
    parser.cur_arg = ti.arg_scope()

def p_arg_list_one(p):
    "arg_list : lpattern_scope lpattern annotation"
    t = None
    print(p[3], type(p[3]))
    if not p[3] or (t := (p[3] & p[2])):
        p[0] = [t]
    else:
        parser.err_type = err.err_types.type
        err.fpy_type_error(make_error_text(p), p[3], p[2], p.lexer.lineno)
        p_error(p)
    parser.cur_arg.update_types(t)
    print("ARG_LIST", parser.code[parser.code.cur_f].scope)
    if v := parser.code[parser.code.cur_f].scope_in_error(parser.cur_arg):
        parser.err_type = err.err_types.redef
        err.name_already_defined(v.name, p.lexer.lineno, v.line)
        p_error(p)

def p_arg_list(p):
    "arg_list : arg_list ',' lpattern_scope lpattern annotation"
    t = p[4]
    if not p[4] or (t := (p[4] & p[5])):
        p[1].append(t)
        p[0] = p[1]
    else:
        parser.err_type = err.err_types.type
        err.fpy_type_error(make_error_text(p), p[5], p[4], p.lexer.lineno)
        p_error(p)
    parser.cur_arg.update_types(t)
    if v := parser.code[parser.code.cur_f].scope_in_error(parser.cur_arg):
        parser.err_type = err.err_types.redef
        err.name_already_defined(v.name, p.lexer.lineno, v.line)
        p_error(p)

def p_prefix(p):
    "prefix : ID"
    parser.code.cur_f = p[1]
    p[0] = p[1]

def p_prefix_special(p):
    "prefix : '[' SPECIALID ']'"
    parser.code.cur_f = p[2]
    p[0] = p[2]

def p_returntype(p):
    "returntype :"
    p[0] = ti.Any_()

def p_returntype_exists(p):
    "returntype : RARROW typedesc"
    p[0] = p[2]

# types
def p_annotation(p):
    "annotation :"
    p[0] = ti.Any_()

def p_annotation_exists(p):
    "annotation : ':' typedesc"
    p[0] = p[2]

def p_typedesc(p):
    """
    typedesc    : typeid
                | typeclass
                | function_type
    """
    p[0] = p[1]

def p_typedesc_tuple(p):
    "typedesc : '(' tuple_type ')'"
    p[0] = ti.tuple_(content=p[2], is_empty=False)

def p_typeclass(p):
    "typeclass : ID ID"
    # neste caso, apenas estas, mas para permitir adicionar mais
    match p[1]:
        case "Num":
            p[0] = ti.Num(generic=p[2])
        case "Eq":
            p[0] = ti.Eq(generic=p[2])
        case "Ord":
            p[0] = ti.Ord(generic=p[2])
        case _:
            parser.err_type = err.err_types.call  # não é, mas serve
            err.fpy_type_error(
                f"{p[1]} {p[2]}",
                "Num, Eq, Ord or Any",
                f"Unknown {p[1]}",
                p.lexer.lineno,
            )
            p_error(p)

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

def p_typeid_char(p):
    "typeid : CHAR"
    p[0] = ti.char_()

def p_typeid_bool(p):
    "typeid : BOOL"
    p[0] = ti.bool_()

def p_typeid_id(p):
    "typeid : ID"
    p[0] = parser.code.check_alias(p[1])

def p_typeid_list(p):
    "typeid : '[' typedesc ']'"
    p[0] = ti.list_(content=p[2], is_empty=False)

# let_blocks
def p_let_block(p):
    "let_block : LET '{' let_cont '}'"
    pass

def p_let_cont(p):
    """let_cont : assign
                | let_cont ',' assign"""
    if v := parser.code[parser.code.cur_f].scope_in_error(parser.cur_arg):
        parser.err_type = err.err_types.redef
        err.name_already_defined(v.name, p.lexer.lineno, v.line)
        p_error(p)

def p_assign(p):
    "assign : lpattern_scope lpattern annotation '=' conditional"
    t = p[2] & p[3] & p[5].type
    if not t and p[2].type.is_empty:
        parser.err_type = err.err_types.type
        err.fpy_type_error(p[3].name, p[3], p[5], p.lexer.lineno)
        p_error(p)
    for v in parser.cur_arg.names:
        if t := parser.code.lvar_in_scope(v):
            parser.err_type = err.err_types.name
            err.name_already_defined(v.name, p.lexer.lineno, v.line)
            p_error(p)
    parser.cur_arg.update_types(p[5])

def p_lpattern(p):
    """
    lpattern : lvar
             | llist
             | ltuple
    """
    p[0] = p[1]

def p_llist_empty(p):
    "llist : '[' ']'"
    p[0] = ti.list_("[]")

def p_llist_patterned(p):
    "llist : '[' pattern_list ']'"
    p[0] = ti.discrete_list(content=p[2])

def p_llist_head_tail(p):
    "llist : '[' lpattern '|' lpattern ']'"
    if p[2] & p[4]:
        p[0] = ti.htlist_(content=p[2], tail=ti.list_(content=p[4]))
    else:
        parser.err_type = err.err_types.type
        err.fpy_type_error(make_error_text(p), p[2], p[4], p.lexer.lineno)
        p_error(p)

def p_pattern_list(p):
    "pattern_list : lpattern"
    p[0] = p[1]

def p_pattern_list_list(p):
    "pattern_list : pattern_list ',' lpattern"
    if t := (p[1] & p[3]):
        p[0] = t
    else:
        parser.err_type = err.err_types.type
        err.fpy_type_error(make_error_text(p), p[1], p[3], p.lexer.lineno)
        p_error(p)

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
    ti.typeclass.generic_count += 1
    parser.cur_arg[p[1]] = ti.variable(p[1], p[0], p.lexer.lineno)

def p_lvar1(p):
    """lvar : '[' SPECIALID ']'
            | '[' OR ']'
            | '[' AND ']'
            | '[' EQ ']'
            | '[' NEQ ']'
            | '[' '>' ']'
            | '[' '<' ']'
            | '[' GTE ']'
            | '[' LTE ']'
            | '[' '+' ']'
            | '[' '-' ']'
            | '[' '*' ']'
            | '[' '/' ']'
            | '[' '^' ']'
            | '[' '%' ']'
            | '[' DIV ']'"""
    p[0] = ti.Any_()
    ti.typeclass.generic_count += 1
    err.impossible_function_case(p[2], p.lexer.lineno)

def p_lvar3(p):
    "lvar : INTT"
    p[0] = ti.int_()
    parser.cur_arg[p[1]] = ti.variable(p[1], p[0], p.lexer.lineno)

def p_lvar4(p):
    "lvar : FLOATT"
    p[0] = ti.float_()
    parser.cur_arg[p[1]] = ti.variable(p[1], p[0], p.lexer.lineno)

def p_lvar5(p):
    "lvar : CHART"
    p[0] = ti.char_()
    parser.cur_arg[p[1]] = ti.variable(p[1], p[0], p.lexer.lineno)

def p_lvar6(p):
    "lvar : BOOLT"
    p[0] = ti.bool_()
    parser.cur_arg[p[1]] = ti.variable(p[1], p[0], p.lexer.lineno)

def p_lvar7(p):
    "lvar : STRINGT"
    p[0] = ti.discrete_list(content=ti.char_())
    parser.cur_arg[p[1]] = ti.variable(p[1], p[0], p.lexer.lineno)

def p_lvar8(p):
    "lvar : '(' lpattern ')'"
    p[0] = p[2]

# condition
def p_condition_undefined(p):
    "conditional : UNDEFINED"
    p[0] = ti.variable(type_=ti.Any_())

def p_conditional_compound(p):
    "conditional : compound"
    p[0] = p[1]

def p_conditional_ifthenelse(p):
    "conditional : IF conditional THEN conditional ELSE conditional"
    if type(p[2].type) == ti.bool_ and (t := (p[4].type % p[6].type)):
        p[0] = t
    else:
        parser.err_type = err.err_types.type
        err.fpy_type_error(make_error_text(p), p[4], p[5])
        p_error(p)

# compound

# OR
def p_compound1(p):
    "compound : or_exp"
    p[0] = p[1]

def p_compound_infix(p):
    "compound : compound OR or_exp"
    p[2] = ti.var_function(name=p[1] ,type_=ti.function_(args=[ti.bool_(), ti.bool_()], return_=ti.bool_()), line=p.lexer.lineno)
    p[0] = infix_case(p[1], p[2], p[3], p)

def p_compound_right_infix(p):
    "compound : '[' compound OR ']'"
    p[2] = ti.var_function(name=p[1] ,type_=ti.function_(args=[ti.bool_(), ti.bool_()], return_=ti.bool_()), line=p.lexer.lineno)
    p[0] = right_infix_case(p[2], p[3], p)

def p_compound_left_infix(p):
    "compound : '[' OR or_exp ']'"
    p[2] = ti.var_function(name=p[1] ,type_=ti.function_(args=[ti.bool_(), ti.bool_()], return_=ti.bool_()), line=p.lexer.lineno)
    p[0] = left_infix_case(p[3], p[2], p)
    # AND

def p_or_exp(p):
    "or_exp : relat"
    p[0] = p[1]

def p_or_exp_infix(p):
    "or_exp : or_exp AND relat"
    p[2] = ti.var_function(name=p[1] ,type_=ti.function_(args=[ti.bool_(), ti.bool_()], return_=ti.bool_()), line=p.lexer.lineno)
    p[0] = infix_case(p[1], p[2], p[3])

def p_or_exp_right_infix(p):
    "or_exp : '[' or_exp AND ']'"
    p[2] = ti.var_function(name=p[1] ,type_=ti.function_(args=[ti.bool_(), ti.bool_()], return_=ti.bool_()), line=p.lexer.lineno)
    p[0] = right_infix_case(p[2], p[3], p)

def p_or_exp_left_infix(p):
    "or_exp : '[' AND relat ']'"
    p[2] = ti.var_function(name=p[1] ,type_=ti.function_(args=[ti.bool_(), ti.bool_()], return_=ti.bool_()), line=p.lexer.lineno)
    p[0] = left_infix_case(p[3], p[2], p)
    # RELAT

def p_relat(p):
    "relat : aritm"
    p[0] = p[1]

def p_relat_infix(p):
    "relat : relat relat_op aritm"
    p[0] = infix_case(p[1], p[2], p[3], p)

def p_relat_right_infix(p):
    "relat : '[' relat relat_op ']'"
    p[0] = right_infix_case(p[2], p[3], p)

def p_relat_left_infix(p):
    "relat : '[' relat_op aritm ']'"    
    p[0] = left_infix_case(p[3], p[2], p)

def p_relat_op(p):
    """relat_op  : EQ
    | NEQ
    | '>'
    | '<'
    | GTE
    | LTE"""
    p[0] = ti.var_function(
        name=p[1],
        type_=ti.function_(
            args=[ti.Eq(generic="a"), ti.Eq(generic="a")], return_=ti.bool_()
        )
        if p[1] in ("==", "!=")
        else ti.function_(
            args=[ti.Ord(generic="a"), ti.Ord(generic="a")], return_=ti.bool_()
        ),
        line=p.lexer.lineno,
    )
    # ARITM

def p_aritm(p):
    "aritm : factor"
    p[0] = p[1]

def p_aritm_infix(p):
    "aritm : aritm aritm_op factor"
    p[0] = infix_case(p[1], p[2], p[3], p)

def p_aritm_right_infix(p):
    "aritm : '[' aritm aritm_op ']'"
    p[0] = right_infix_case(p[2], p[3], p)

def p_aritm_left_infix(p):
    "aritm : '[' aritm_op factor ']'"
    p[0] = left_infix_case(p[3], p[2], p)

def p_aritm_op(p):
    """
    aritm_op : '+'
             | '-'
    """
    p[0] = ti.var_function(
        name=p[1],
        type_=ti.function_(
            args=[ti.Num(generic="a"), ti.Num(generic="a")], return_=ti.Num(generic="a")
        ),
        line=p.lexer.lineno,
    )
    # FACTOR

def p_factor(p):
    "factor : pow"
    p[0] = p[1]

def p_factor_infix(p):
    "factor : factor factor_op pow"
    p[0] = infix_case(p[1], p[2], p[3], p)

def p_factor_right_infix(p):
    "factor : '[' factor factor_op ']'"
    p[0] = right_infix_case(p[2], p[3], p)

def p_factor_left_infix(p):
    "factor : '[' factor_op pow ']'"
    p[0] = left_infix_case(p[3], p[2], p)

def p_factor_op(p):
    """factor_op : '*'
                 | '/'
                 | '%'
                 | DIV"""
    type_ = None
    match p[1]:
        case "*":
            type_ = ti.function_(
                args=[ti.Num(generic="a"), ti.Num(generic="a")],
                return_=ti.Num(generic="a"),
            )
        case "/":
            type_ = ti.function_(args=[ti.float_(), ti.float_()], return_=ti.float_())
        case _:
            type_ = ti.function_(args=[ti.int_(), ti.int_()], return_=ti.int_())
    p[0] = ti.var_function(name=p[1], type_=type_, line=p.lexer.lineno)

# TODO: continua aqui
# POW
def p_pow(p):
    "pow : rest"
    p[0] = p[1]

def p_pow_infix(p):
    "pow : pow '^' rest"
    p[2] = ti.function_(args=[ti.float_(), ti.float_()], return_=ti.float_())
    p[0] = infix_case(p[1], p[2], p[3], p)

def p_pow_right_infix(p):
    "pow : '[' pow '^' ']'"
    p[2] = ti.function_(args=[ti.float_(), ti.float_()], return_=ti.float_())
    p[0] = right_infix_case(p[2], p[3], p)

def p_pow_left_infix(p):
    "pow : '[' '^' rest ']'"
    p[2] = ti.function_(args=[ti.float_(), ti.float_()], return_=ti.float_())
    p[0] = left_infix_case(p[3], p[2], p)
    # REST

def p_rest(p):
    "rest : single"
    p[0] = p[1]

def p_rest_infix(p):
    "rest : rest infix single"
    p[0] = infix_case(p[1], p[2], p[3], p)

def p_rest_right_infix(p):
    "rest : '[' infix single ']'"
    p[0] = right_infix_case(p[2], p[3], p)

def p_rest_left_infix(p):
    "rest : '[' rest infix ']'"
    p[0] = left_infix_case(p[3], p[2], p)

def p_infix1(p):
    "infix : '`' ID '`'"
    p[0] = parser.code.func_body_id(p[2], p.lexer.lineno)

def p_infix2(p):
    "infix : SPECIALID"
    p[0] = parser.code.func_body_id(p[1], p.lexer.lineno)

# single
def p_single(p):
    """single : multivar
              | lambda
              | cond_block"""
    p[0] = p[1]

# cond_block
def p_cond_block(p):
    "cond_block : COND '{' cond ',' ELSE ':' conditional '}'"
    if not (t := (p[3].type & p[7].type)):
        parser.err_type = err.err_types.type
        err.fpy_type_error(make_error_text(p), p[7], p[3], p.lexer.lineno)
        p_error(p)
    p[7].type = t
    p[0] = p[7]

def p_cond(p):
    "cond : cond_singl"
    p[0] = p[1]

def p_cond_list(p):
    "cond : cond ',' cond_singl"
    if not (t := (p[1].type & p[2].type)):
        parser.err_type = err.err_types.type
        err.fpy_type_error(make_error_text(p), p[3], p[1], p.lexer.lineno)
        p_error(p)
    p[1].type = t
    p[0] = p[1]

def p_cond_singl(p):
    "cond_singl : conditional ':' conditional"
    if not p[1].type & ti.bool_():
        parser.err_type = err.err_types.type
        err.fpy_type_error(make_error_text(p), ti.bool_(), p[1], p.lexer.lineno)
        p_error(p)
    p[0] = p[3]

# lambda
def p_lambda_no_args(p):
    "lambda : FDEF '(' ')' '{' conditional '}'"
    p[0] = p[5]

def p_lambda_args(p):
    "lambda : FDEF '(' lambda_scope arg_list ')' '{' conditional '}'"
    del parser.code[parser.code.cur_f]
    parser.code.cur_f = p[3]
    p[0] = ti.var_function(
        type_=ti.function_(return_=p[7].type, args=p[4]), line=p.lexer.lineno, is_id=False
    )

def p_lambda_scope(p):
    r"lambda_scope :"
    cur_scope = {}
    if parser.code.cur_f:
        cur_scope = {x: y for x,y in parser.code[parser.code.cur_f].scope.items()}
    new_name = parser.code.cur_f + '_anonym'
    parser.code[new_name] = ti.function_info(type_=ti.Any_(), line=p.lexer.lineno)
    parser.code[new_name].scope = cur_scope
    p[0] = parser.code.cur_f
    parser.code.cur_f = new_name

# multivar
def p_primaryvar(p):
    """
    multivar    : primaryvar
                | rlist
                | rtuple
    """
    p[0] = p[1]

def p_multivar_call_empty(p):
    "multivar : multivar '(' ')'"
    err.empty_call(p.lexer.lineno)


def p_multivar_call(p):
    "multivar : multivar '(' condition_list ')'"
    f: ti.var_function = None
    needs_check = isinstance(p[1].type, ti.function_)
    name = p[1].name
    print("MULTIVAR", needs_check, p[1])
# TODO: MELHORAR A VERIFICAÇÃO DE ERROS DESTA FUNÇÃO!!! NESTE SÍTIO!!!
    if not (f := p[1].promote(p[3])):
        parser.err_type = err.err_types.call
        err.non_callable(p[1].name, p[1].type, p.lexer.lineno)
        p_error(p)
    if needs_check and not (v := f.verify_args(p[3])):
        parser.err_type = err.err_types.type
        err.fpy_type_error(make_error_text(p), p[1].type, v[1].type, p.lexer.lineno)
        p_error(p)
    if not (err_ := parser.code.update_variable_type(f))[0]:
        parser.err_type = err.err_types.redef
        err_size_check = len(err_) == 1
        err.name_already_defined(
            name if name else make_error_text(p),
            '*no information*' if err_size_check else err_[1].line,
            p.lexer.lineno
        )
        p_error(p)
    v = None
    f = f.modulo(p[3])
    p[0] = f

# rtuple
def p_rtuple_empty(p):
    "rtuple : '(' ')'"
    p[0] = ti.variable(name="()", type_=ti.tuple(), line=p.lexer.lineno, is_id=True)

def p_rtuple_cont(p):
    "rtuple : '(' rtuple_cont ')'"
    p[0] = ti.make_tuple(p[2], p.lexer.lineno)

def p_rtuple_cont_2_case(p):
    "rtuple_cont : conditional ',' conditional"
    p[0] = [p[1], p[3]]

def p_rtuple_cont_rest_case(p):
    "rtuple_cont : rtuple_cont ',' conditional"
    p[1].append(p[3])
    p[0] = p[1]

# rlist
def p_rlist_empty(p):
    "rlist : '[' ']'"
    p[0] = ti.variable(name="[]", type_=ti.list_(), line=p.lexer.lineno, is_id=True)

def p_rlist_normal(p):
    "rlist : '[' condition_list ']'"
    if not (t := reduce(lambda x, y: x & y, [x.type for x in p[2]])):
        parser.err_type = err.err_types.type
        err.fpy_type_error(make_error_text(p), p[2][0], p[2][-1], p.lexer.line)
        p_error(p)
    p[0] = ti.make_discrete_list(t, p.lexer.lineno)

def p_rlist_condition_list(p):
    "rlist : '[' conditional '|' conditional ']'"
    type_p4 = type(p[4].type)
    if (
        issubclass(type_p4, ti.typeclass)
        or (type_p4 == ti.function_ and p[2].type & p[4].type.return_)
        or p[2].type & p[4].type
    ):
        p[0] = ti.make_htlist(p[2], p[4] , p.lexer.lineno)
    else:
        parser.err_type = err.err_types.type
        err.fpy_type_error(
            f"[{p[2].name}|{p[4].name}]", ti.list_(content=p[2].type), p[4].type if p[4].type else "Any -> ?", p.lexer.lineno
        )
        p_error(p)

def p_rlist_ranger(p):
    "rlist : '[' conditional RANGER conditional ']'"
    if p[2].type & ti.int_() and p[4].type & ti.int_():
        p[0] = ti.variable(name=f"[{p[2]}..{p[4]}]", type_=ti.discrete_list(content=ti.int_(), is_empty=False), line=p.lexer.lineno)
    else:
        parser.err_type = err.err_types.type
        err.fpy_type_error(
            f"[{p[2]}..{p[4]}]", ti.list_(content=ti.int_()), f"{p[2].type}: ?", p.lexer.lineno
        )
        p_error(p)

def p_rlist_condition_list_conditional(p):
    "condition_list : conditional"
    p[0] = [p[1]]

def p_rlist_condition_list_list(p):
    "condition_list : condition_list ',' conditional"
    if p[1][-1].type & p[3].type:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        parser.err_type = err.err_types.type
        err.fpy_type_error(make_error_text(p), p[1], p[3], p.lexer.lineno)
        p_error(p)

# primaryvar
def p_primaryvar_ID(p):
    "primaryvar : ID"
    p[0] = parser.code.func_body_id(p[1], p.lexer.lineno)

def p_primaryvar_int(p):
    "primaryvar : INTT"
    p[0] = ti.variable(name=p[1], type_=ti.int_(name=p[1]), line=p.lexer.lineno)

def p_primaryvar_string(p):
    "primaryvar : STRINGT"
    p[0] = ti.variable(
        name=p[1],
        type_=ti.discrete_list(name=p[1], content=ti.char_(), is_empty=p[1] == '""'),
        line=p.lexer.lineno,
    )

def p_primaryvar_float(p):
    "primaryvar : FLOATT"
    p[0] = ti.variable(name=p[1], type_=ti.float_(name=p[1]), line=p.lexer.lineno)

def p_primaryvar_char(p):
    "primaryvar : CHART"
    p[0] = ti.variable(name=p[1], type_=ti.char_(name=p[1]), line=p.lexer.lineno)

def p_primaryvar_bool(p):
    "primaryvar : BOOLT"
    p[0] = ti.variable(name=p[1], type_=ti.bool_(name=p[1]), line=p.lexer.lineno)

def p_primaryvar_SPECIALID(p):
    "primaryvar : '[' SPECIALID ']'"
    p[0] = parser.code.func_body_id(p[2], p.lexer.lineno)

def p_primaryvar_OR_AND(p):
    """primaryvar : '[' OR ']'
                  | '[' AND ']'"""
    p[0] = ti.var_function(
        name=p[2],
        type_=ti.function_(args=[ti.bool_(), ti.bool_()], return_=ti.bool_()),
        line=p.lexer.lineno,
    )

def p_primaryvar_DIVMOD(p):
    """primaryvar : '[' DIV ']'
                  | '[' '%' ']'"""
    p[0] = ti.var_function(
        name=p[2],
        type_=ti.function_(args=[ti.int_(), ti.int_()], return_=ti.int_()),
        line=p.lexer.lineno,
    )

def p_primaryvar_POWFRAC(p):
    """primaryvar : '[' '/' ']'
                  | '[' '^' ']'"""
    p[0] = ti.var_function(
        name=p[2],
        type_=ti.function_(args=[ti.float_(), ti.float_()], return_=ti.float_()),
        line=p.lexer.lineno,
    )

def p_primaryvar_ARITM(p):
    """
    primaryvar : '[' '+' ']'
               | '[' '-' ']'
               | '[' '*' ']'
    """
    p[0] = ti.var_function(
        name=p[2],
        type_=ti.function_(
            args=[ti.Num(generic="a"), ti.Num(generic="a")], return_=ti.Num(generic="a")
        ),
        line=p.lexer.lineno,
    )

def p_primaryvar_N_EQ(p):
    """
    primaryvar : '[' EQ ']'
               | '[' NEQ ']'
    """
    p[0] = ti.var_function(
        name=p[2],
        type_=ti.function_(
            args=[ti.Eq(generic="a"), ti.Eq(generic="a")], return_=ti.bool_()
        ),
        line=p.lexer.lineno,
    )

def p_primaryvar_ORD(p):
    """primaryvar : '[' '<' ']'
                  | '[' '>' ']'
                  | '[' LTE ']'
                  | '[' GTE ']'"""
    p[0] = ti.var_function(
        name=p[2],
        type_=ti.function_(
            args=[ti.Ord(generic="a"), ti.Ord(generic="a")], return_=ti.bool_()
        ),
        line=p.lexer.lineno,
    )

def p_primaryvar_conditional(p):
    "primaryvar : '(' conditional ')'"
    p[0] = p[2]

# INFIXES

def right_infix_case(operand, operator, p):
    op, operator_new_type = ti.right_infix_checker(operator, operand)
    if not op and not operator_new_type:
        parser.err_type = err.err_types.type
        err.fpy_type_error(operand.name, operand.type, "Any -> ?", p.lexer.lineno)
        p_error(p)
    h, *t = parser.code.update_variable_type(operator)
    if not h:
        parser.err_type = err.err_types.type
        err.name_already_defined(
            operator_new_type.name, p.lexer.lineno, t[0].p.lexer.lineno
        )
        p_error(p)        
    return op

def left_infix_case(operand, operator, p):
    op, operator_new_type = ti.left_infix_checker(operator, operand)
    if not op and not operator_new_type:
        parser.err_type = err.err_types.type
        err.fpy_type_error(operator.name, operator.type, "Any -> ?", p.lexer.lineno)
        p_error(p)
    h, *t = parser.code.update_variable_type(operator)
    if not h:
        parser.err_type = err.err_types.type
        err.name_already_defined(
            operator_new_type.name, p.lexer.lineno, t[0].line
        )
        p_error(p)
    return op

def infix_case(operand1, operator, operand2, p):
    op, opr1, opr2 = ti.infix_checker(operand1, operator, operand2)
    if not all((op, opr1, opr2)):
        parser.err_type = err.err_types.type
        err.fpy_type_error(f"{operand1.name} {operator.name} {operand2.name}", operator.type, f"{operand1.type} -> {operand2.type}", p.lexer.lineno)
        p_error(p)
    for type_, old in ((opr1, operand1), (opr2, operand2)):
        old.type = type_
        h, *t = parser.code.update_variable_type(old)
        if not type_ and not h:
            parser.err_type = err.err_types.type
            err.name_already_defined(
                old.name, p.lexer.lineno, old.p.lexer.lineno
            )
            p_error(p)
    return op

# ERRORS
lexpos = lambda p: p.lexer.lexpos - p.lexer.dif + 1

def p_error(p):
    if parser.code.cur_f:
        parser.code[parser.code.cur_f].scope = {}
    if not p:
        pass
    match parser.err_type:
        case err.err_types.redef | err.err_types.name | err.err_types.call | err.err_types.type | err.err_types.scope:
            raise SyntaxError
        case _:
            print(
                f"Parse error with '{err.red_bold(p)}' on line {p.lexer.lineno}:{lexpos(p)}"
            )

# def on_type_error(p):
    # if not p:
        # pass
    # tok = parser.token()
    # while tok and tok.type == "RBRACE":
        # tok = parser.token()
    # parser.err_type = None
    # parser.errok()

parser = yacc.yacc()
parser.code: ti.code_ = ti.code_()
parser.err_type = None
parser.code.cur_arg = None

def make_error_text(p):
    cur_err = code__[p.lexer.lineno - 1][(p.lexer.lexpos - p.lexer.dif + 1) :]
    return cur_err if len(cur_err) < 20 else f"{cur_err[:20]}..."

def parse_types(code):
    global code__
    stdlib = open("./code_construction/fpystdlib.py", "r").read()
    code__ = stdlib.split("\n")
    parser.parse(stdlib)
    parser.restart()
    lexer.lineno = 1
    code__ = code.split("\n")
    parser.parse(code)

# testing
if __name__ == "__main__":
    code = sys.stdin.read()
    parse_types(code)
