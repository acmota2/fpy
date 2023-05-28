import sys
from lexer import tokens, literals, lexer
import ply.yacc as yacc
from code_construction.function import ffunction
import code_construction.fpystdlib as std
import re

infix_token_pairs = {
    '*': '*',
    '/': '/',
    '//': '//',
    '%': '%',
    '^': '**',
    '+': '+',
    '-': '-',
    '==': '==',
    '!=': '!=',
    '>': '>',
    '<': '<',
    '<=': '<=',
    '>=': '>=',
    '&&': 'and',
    '||': 'or'
}
i = 0
infix_function_pairs = {
    '*':        std.mul,
    '/':        std.frac,
    '//':       std.div,
    '%':        std.mod,
    '^':        std.ppow,
    '+':        std.add,
    '-':        std.sub,
    '==':       std.eq,
    '!=':       std.neq,
    '>':        std.gt,
    '<':        std.lt,
    '<=':       std.lte,
    '>=':       std.gte,
    '&&':       std.aand,
    '||':       std.oor,
    "from_int": std.from_int,
    "not":      std.nnot,
    ".":        "std.compose",
    "++":       "std.concatenate",
    "><":       "std.func_prod",
    "foldr":    "std.foldr",
    "foldl":    "std.foldl",
    "map":      "std.map_",
    "filter":   "std.filter_",
    "concat":   "std.concat"
}

reserved_funcs = {"filter_", "map_", "concat", "foldl", "foldr", "concatenate", "func_prod", "compose"}

scope_vars = (set(), None)

fs = {}

def p_all(p):
    "all : "
    p[0] = """print("NAO ESCREVESTE CODIGO. NMSE!")"""

def p_all1(p):
    "all : BEGIN END"
    p[0] = """print("NAO ESCREVESTE CODIGO. NMSE!")"""

def p_all2(p):
    "all : BEGIN body END"
    s = "" # maybe needs changes
    written_fs = set()
    for statement, isFunc in p[2]:
        if isFunc and not statement in written_fs:
            s += fs[statement].buildString()
            written_fs.add(statement)
        elif not statement in written_fs:
            s += statement
        s += "\n"
    p[0] = s

def p_body(p):
    "body : statement"
    p[0] = [p[1]] if not p[1] is None else []

def p_body1(p):
    "body : body statement"
    p[0] = p[1] + [p[2]] if not p[1] is None else p[1]

def p_statement(p):
    "statement : function"
    p[0] = (p[1], True)

# ? Type hinting so que nao
def p_statement1(p):
    "statement : ALIAS ID '=' typedesc"
    pass

# Variavel global
def p_statement2(p):
    "statement : LET ID annotation '=' conditional"
    p[0] = (f"""{p[2]} = lambda: {p[5]}""", False)



def p_function(p):
    "function : scope conditional '}'"
    f = (p[1][0], p[1][1], p[1][2], p[2])
    if not f[0] in fs:
        fs[f[0]] = ffunction(f[0], f[1], f[2], f[3])
    else:
        fs[f[0]].addDefinition(f[1], f[2], f[3])
    p[0] = f[0]

def p_scope(p):
    "scope : main_scope"
    p[0] = (p[1][0], p[1][1], None)

def p_scope1(p):
    "scope : main_scope let_block"
    p[0] = (p[1][0], p[1][1], p[2])

def p_main_scope(p):
    "main_scope : new_f args returntype '{'"
    p[0] = (p[1], p[2])

def p_new_f(p):
    "new_f : FDEF prefix"
    p[0] = p[2]
    global scope_vars
    scope_vars = (set(), None)

def p_args(p):
    "args : '(' ')'"
    p[0] = "()"

def p_args1(p):
    "args : '(' arg_list ')'"
    p[0] = f"""{p[2]}"""

def p_lpattern_scope(p):
    "lpattern_scope : "
    pass

def p_arg_list(p):
    "arg_list : lpattern_scope lpattern annotation"
    global scope_vars
    scope_vars[0].add(p[2])
    p[0] = p[2]

def p_arg_list1(p):
    "arg_list : arg_list ',' lpattern_scope lpattern annotation"
    global scope_vars
    scope_vars[0].add(p[4])
    p[0] = f"""{p[1]}, {p[4]}"""

def p_prefix(p):
    "prefix : ID"
    p[0] = p[1]

def p_prefix1(p):
    "prefix : '[' SPECIALID ']'"
    global i
    if not p[2] in infix_function_pairs:
        i+=1
        p[0] = f"infix{i-1}"
        infix_function_pairs[p[2]] = p[0]
    else:
        p[0] = infix_function_pairs[p[2]]



def p_returntype(p):
    "returntype : "
    pass

def p_returntype1(p):
    "returntype : RARROW typedesc"
    pass

def p_annotation(p):
    "annotation : "
    pass

def p_annotation1(p):
    "annotation : ':' typedesc"
    pass

def p_typedesc(p):
    "typedesc : typeid"
    pass

def p_typedesc1(p):
    "typedesc : typeclass"
    pass

def p_typedesc2(p):
    "typedesc : function_type"
    pass

def p_typedesc3(p):
    "typedesc : '(' tuple_type ')'"
    pass

def p_typeclass(p):
    "typeclass : ID ID"
    pass

def p_function_type(p):
    "function_type : '(' typedesc ')' RARROW typedesc"
    pass

def p_function_type1(p):
    "function_type : '(' tuple_type ')' RARROW typedesc"
    pass

def p_tuple_type(p):
    "tuple_type : typeid ',' typeid"
    pass

def p_tuple_type1(p):
    "tuple_type : tuple_type ',' typeid"
    pass

def p_typeid(p):
    "typeid : INT"
    pass

def p_typeid1(p):
    "typeid : FLOAT"
    pass

def p_typeid2(p):
    "typeid : CHAR"
    pass

def p_typeid3(p):
    "typeid : BOOL"
    pass

def p_typeid4(p):
    "typeid : ID"
    pass

def p_typeid5(p):
    "typeid : '[' typedesc ']'"
    pass

def p_let_block(p):
    "let_block : LET '{' let_cont '}'"
    p[0] = p[3]

def p_let_cont(p):
    "let_cont : assign"
    p[0] = p[1]

def p_let_cont1(p):
    "let_cont : let_cont ',' assign"
    p[0] = f"{p[1]}; {p[3]}"

def p_assign(p):
    "assign : lpattern annotation '=' conditional"
    global scope_vars
    scope_vars[0].add(p[1])
    p[0] = f"{p[1]} = {p[4]}"

def p_lpattern(p):
    "lpattern : lvar"
    p[0] = p[1]

def p_lpattern1(p):
    "lpattern : llist"
    p[0] = p[1]

def p_lpattern2(p):
    "lpattern : ltuple"
    p[0] = p[1]

def p_llist(p):
    "llist : '[' ']'"
    p[0] = "[]"

def p_llist1(p):
    "llist : '[' pattern_list ']'"
    p[0] = f"[{p[2]}]"
    global scope_vars
    scope_vars[0].add(p[2])

def p_llist2(p):
    "llist : '[' lpattern '|' lpattern ']'"
    p[0] = f"[{p[2]}, *{p[4]}]"
    global scope_vars
    scope_vars[0].add(p[2])
    scope_vars[0].add(p[4])

def p_pattern_list(p):
    "pattern_list : lpattern"
    p[0] = p[1]
    global scope_vars
    scope_vars[0].add(p[1])

def p_pattern_list1(p):
    "pattern_list : pattern_list ',' lpattern"
    p[0] = f"{p[1]}, {p[3]}"
    global scope_vars
    scope_vars[0].add(p[3])

def p_ltuple(p):
    "ltuple : '(' ')'"
    p[0] = "()"

def p_ltuple1(p):
    "ltuple : '(' ltuple_cont ')'"
    p[0] = f"({p[2]})"
    global scope_vars
    scope_vars[0].add(p[2])

def p_ltuple_cont(p):
    "ltuple_cont : lpattern ',' lpattern"
    p[0] = f"""{p[1]}, {p[3]}"""
    global scope_vars
    scope_vars[0].add(p[1])
    scope_vars[0].add(p[3])

def p_ltuple_cont1(p):
    "ltuple_cont : ltuple_cont ',' lpattern"
    p[0] = f"""{p[1]}, {p[3]}"""
    global scope_vars
    scope_vars[0].add(p[3])

def p_lvar(p):
    "lvar : ID"
    p[0] = p[1]

def p_lvar1(p):
    "lvar : STRINGT"
    p[0] = p[1]

def p_lvar2(p):
    "lvar : INTT"
    p[0] = p[1]

def p_lvar3(p):
    "lvar : FLOATT"
    p[0] = p[1]

def p_lvar4(p):
    "lvar : CHART"
    p[0] = p[1]

def p_lvar5(p):
    "lvar : BOOLT"
    p[0] = p[1]

def p_lvar6(p):
    "lvar : '[' SPECIALID ']'"
    p[0] = infix_token_pairs[p[2]]

def p_lvar7(p):
    "lvar : '[' OR ']'"
    p[0] = infix_token_pairs[p[2]]

def p_lvar8(p):
    "lvar : '[' AND ']'"
    p[0] = infix_token_pairs[p[2]]

def p_lvar9(p):
    "lvar : '[' EQ ']'"
    p[0] = infix_token_pairs[p[2]]

def p_lvar10(p):
    "lvar : '[' NEQ ']'"
    p[0] = infix_token_pairs[p[2]]

def p_lvar11(p):
    "lvar : '[' '>' ']'"
    p[0] = infix_token_pairs[p[2]]

def p_lvar12(p):
    "lvar : '[' '<' ']'"
    p[0] = infix_token_pairs[p[2]]

def p_lvar13(p):
    "lvar : '[' GTE ']'"
    p[0] = infix_token_pairs[p[2]]

def p_lvar14(p):
    "lvar : '[' LTE ']'"
    p[0] = infix_token_pairs[p[2]]

def p_lvar15(p):
    "lvar : '[' '+' ']'"
    p[0] = infix_token_pairs[p[2]]

def p_lvar16(p):
    "lvar : '[' '-' ']'"
    p[0] = infix_token_pairs[p[2]]

def p_lvar17(p):
    "lvar : '[' '*' ']'"
    p[0] = infix_token_pairs[p[2]]

def p_lvar18(p):
    "lvar : '[' '/' ']'"
    p[0] = infix_token_pairs[p[2]]

def p_lvar19(p):
    "lvar : '[' '^' ']'"
    p[0] = infix_token_pairs[p[2]]

def p_lvar20(p):
    "lvar : '[' '%' ']'"
    p[0] = infix_token_pairs[p[2]]

def p_lvar21(p):
    "lvar : '[' DIV ']'"
    p[0] = infix_token_pairs[p[2]]

def p_lvar22(p):
    "lvar : '(' lpattern ')'"
    p[0] = p[2]

def p_conditional(p):
    "conditional : UNDEFINED"
    pass

def p_conditional1(p):
    "conditional : compound"
    p[0] = p[1]

def p_conditional2(p):
    "conditional : IF conditional THEN conditional ELSE conditional"
    p[0] = f"{p[4]} if {p[2]} else {p[6]}"

def p_compound(p):
    "compound : compound OR or_exp"
    p[0] = f"({p[1]} or {p[3]})"

def p_compound1(p):
    "compound : or_exp"
    p[0] = p[1]

def p_compound2(p):
    "compound : '[' compound OR ']'"
    p[0] = f"lambda x: {p[2]} or x"


def p_compound3(p):
    "compound : '[' OR or_exp ']'"
    p[0] = f"lambda x: x or {p[3]}"

def p_or_exp(p):
    "or_exp : or_exp AND relat"
    p[0] = f"{p[1]} and {p[3]}"

def p_or_exp1(p):
    "or_exp : relat"
    p[0] = p[1]

def p_or_exp2(p):
    "or_exp : '[' or_exp AND ']'"
    p[0] = f"lambda x: {p[2]} and x"

def p_or_exp3(p):
    "or_exp : '[' AND relat ']'"
    p[0] = f"lambda x: x and {p[3]}"

def p_relat(p):
    "relat : relat relat_op aritm"
    p[0] = f"({p[1]} {p[2]} {p[3]})"

def p_relat1(p):
    "relat : aritm"
    p[0] = p[1]

def p_relat2(p):
    "relat : '[' relat relat_op ']'"
    p[0] = f"lambda x: {p[2]} {p[3]} x"

def p_relat3(p):
    "relat : '[' relat_op aritm ']'"
    p[0] = f"lambda x: x {p[2]} {p[3]}"

def p_relat_op(p):
    "relat_op : EQ"
    p[0] = "=="

def p_relat_op1(p):
    "relat_op : NEQ"
    p[0] = "!="

def p_relat_op2(p):
    "relat_op : '>'"
    p[0] = ">"

def p_relat_op3(p):
    "relat_op : '<'"
    p[0] = "<"

def p_relat_op4(p):
    "relat_op : GTE"
    p[0] = ">="

def p_relat_op5(p):
    "relat_op : LTE"
    p[0] = "<="

def p_aritm(p):
    "aritm : aritm aritm_op factor"
    p[0] = f"({p[1]} {p[2]} {p[3]})"

def p_aritm1(p):
    "aritm : factor"
    p[0] = p[1]

def p_aritm2(p):
    "aritm : '[' aritm aritm_op ']'"
    p[0] = f"lambda x: {p[2]} {p[3]} x"

def p_aritm3(p):
    "aritm : '[' aritm_op factor ']'"
    p[0] = f"lambda x: x {p[2]} {p[3]}"

def p_aritm_op(p):
    "aritm_op : '+'"
    p[0] = "+"

def p_aritm_op1(p):
    "aritm_op : '-'"
    p[0] = "-"

def p_factor(p):
    "factor : factor factor_op pow"
    p[0] = f"({p[1]} {p[2]} {p[3]})"

def p_factor1(p):
    "factor : pow"
    p[0] = p[1]

def p_factor2(p):
    "factor : '[' factor factor_op ']'"
    p[0] = f"lambda x: {p[2]} {p[3]} x"

def p_factor3(p):
    "factor : '[' factor_op pow ']'"
    p[0] = f"lambda x: x {p[2]} {p[3]}"

def p_factor_op(p):
    "factor_op : '*'"
    p[0] = "*"

def p_factor_op1(p):
    "factor_op : '/'"
    p[0] = "/"

def p_factor_op2(p):
    "factor_op : '%'"
    p[0] = "%"

def p_factor_op3(p):
    "factor_op : DIV"
    p[0] = "//"

def p_pow(p):
    "pow : pow '^' rest"
    p[0] = f"({p[0]} ** {p[1]})"

def p_pow1(p):
    "pow : rest"
    p[0] = p[1]

def p_pow2(p):
    "pow : '[' pow '^' ']'"
    p[0] = f"lambda x: {p[2]} ** x"

def p_pow3(p):
    "pow : '[' '^' rest ']'"
    p[0] = f"lambda x: x ** {p[3]}"

def p_rest(p):
    "rest : rest infix single"
    p[0] = f"({p[2]}({p[1]},{p[3]}))"

def p_rest1(p):
    "rest : single"
    p[0] = p[1]

def p_rest2(p):
    "rest : '[' rest infix ']'"
    p[0] = f"{p[3]}({p[2]}, x)"

def p_rest3(p):
    "rest : '[' infix single ']'"
    p[0] = f"{p[2]}(x, {p[3]})"

def p_infix(p):
    "infix : '`' ID '`'"
    p[0] = p[2]

def p_infix1(p):
    "infix : SPECIALID"
    p[0] = infix_function_pairs[p[1]]

def p_single(p):
    "single : multivar"
    p[0] = p[1]

def p_single1(p):
    "single : lambda"
    p[0] = p[1]

def p_single2(p):
    "single : cond_block"
    p[0] = p[1]

def p_cond_block(p):
    "cond_block : COND '{' cond ',' ELSE ':' conditional '}'"
    p[0] = f"({p[3][0]} ({p[7]}){p[3][1]*')'})"

def p_cond(p):
    "cond : cond_singl"
    p[0] = (p[1], 1)

def p_cond1(p):
    "cond : cond ',' cond_singl"
    p[0] = (f"{p[1][0]} {p[2]}", p[1][1] + 1)

def p_cond_singl(p):
    "cond_singl : conditional ':' conditional"
    p[0] = f"{p[3]} if {p[1]} else ("

def p_lambda(p):
    "lambda : FDEF '(' ')' '{' conditional '}' "
    p[0] = f"lambda: {p[5]}"

def p_lambda1(p):
    "lambda : FDEF '(' lambda_scope arg_list ')' '{' conditional '}'"
    l_vars = re.sub(r"[\s\[\]]", "", p[4]).split(",")
    i = 0
    for v in l_vars:
        to_sub = ""
        if v[0] == "*":
            to_sub = f"____t[{i}:]"
            v = v[1:]
        else:
            to_sub = f"____t[{i}]" 
        pattern = fr"\b{v}\b"
        p[7] = re.sub(pattern, to_sub, p[7])
        i+=1
    p[0] = f"lambda ____t: {p[7]}"
    global scope_vars
    scope_vars = scope_vars[1]
    pass


def p_lambda_scope(p):
    "lambda_scope : "
    global scope_vars
    scope_vars = (set(scope_vars[0]), scope_vars)
    pass

#chamada de funcao sem argumentos
def p_multivar(p):
    "multivar : multivar '(' ')'"
    p[0] = re.sub(r"\(([a-zA-Z_][\w\.]*\([a-zA-Z_][\w\.]*, [a-zA-Z_][\w\.]*\))\)\(\)", "\1",f"""{p[1]}()""")

#chamada de funcao com lista de argumentos
def p_multivar1(p):
    "multivar : multivar '(' condition_list ')'"
    p[0] = re.sub(r"\(([a-zA-Z_][\w\.]*)\(([a-zA-Z_][\w\.]*),([a-zA-Z_][\w\.]*)\)\)\((.*)\)", r"\1(\2, \3, \4)",f"""{p[1]}({p[3]})""")

def p_multivar2(p):
    "multivar : rlist"
    p[0] = f"{p[1]}"

def p_multivar3(p):
    "multivar : rtuple"
    p[0] = p[1]

def p_multivar4(p):
    "multivar : primaryvar"
    p[0] = p[1]

def p_rlist(p):
    "rlist : '[' ']'"
    p[0] = "[]"

def p_rlist1(p):
    "rlist : '[' condition_list ']'"
    p[0] = f"[{p[2]}]"

def p_rlist2(p):
    "rlist : '[' conditional '|' conditional ']'"
    p[0] = f"""[{p[2]}] + {p[4]}"""

def p_rlist3(p):
    "rlist : '[' conditional RANGER conditional ']'"
    p[0] = f"""list(range({p[2]}, {int(p[4]) + 1}))"""

def p_condition_list(p):
    "condition_list : conditional"
    p[0] = f"""{p[1]}"""

def p_condition_list1(p):
    "condition_list : condition_list ',' conditional"
    p[0] = f"""{p[1]}, {p[3]}"""

def p_rtuple(p):
    "rtuple : '(' ')'"
    p[0] = "()"

def p_rtuple1(p):
    "rtuple : '(' rtuple_cont ')'"
    p[0] = f"""({p[2]})"""

def p_rtuple_cont(p):
    "rtuple_cont : conditional ',' conditional"
    p[0] = f"""{p[1]}, {p[3]}"""

def p_rtuple_cont1(p):
    "rtuple_cont : rtuple_cont ',' conditional"
    p[0] = f"""{p[1]}, {p[3]}"""

def p_primaryvar(p):
    "primaryvar : ID"
    global scope_vars
    if p[1] in infix_function_pairs:
        p[0] = f"({infix_function_pairs[p[1]]})"
    elif p[1] in scope_vars[0] or p[1] in reserved_funcs:
        p[0] = f"{p[1]}"
    else:
        p[0] = f"{p[1]}()"

def p_primaryvar1(p):
    "primaryvar : INTT"
    p[0] = f"{p[1]}"

def p_primaryvar2(p):
    "primaryvar : FLOATT"
    p[0] = f"{p[1]}"

def p_primaryvar3(p):
    "primaryvar : CHART"
    p[0] = f"{p[1]}"

def p_primaryvar4(p):
    "primaryvar : STRINGT"
    p[0] = f"{p[1]}"

def p_primaryvar5(p):
    "primaryvar : BOOLT"
    p[0] = f"{p[1]}"

def p_primaryvar6(p):
    "primaryvar : '[' SPECIALID ']'"
    p[0] = infix_function_pairs[p[2]]

def p_primaryvar7(p):
    "primaryvar : '[' OR ']'"
    p[0] = infix_function_pairs[p[2]]

def p_primaryvar8(p):
    "primaryvar : '[' AND ']'"
    p[0] = infix_function_pairs[p[2]]

def p_primaryvar9(p):
    "primaryvar : '[' EQ ']'"
    p[0] = infix_function_pairs[p[2]]

def p_primaryvar10(p):
    "primaryvar : '[' NEQ ']'"
    p[0] = infix_function_pairs[p[2]]

def p_primaryvar11(p):
    "primaryvar : '[' '>' ']'"
    p[0] = infix_function_pairs[p[2]]

def p_primaryvar12(p):
    "primaryvar : '[' '<' ']'"
    p[0] = infix_function_pairs[p[2]]

def p_primaryvar13(p):
    "primaryvar : '[' GTE ']'"
    p[0] = infix_function_pairs[p[2]]

def p_primaryvar14(p):
    "primaryvar : '[' LTE ']'"
    p[0] = infix_function_pairs[p[2]]

def p_primaryvar15(p):
    "primaryvar : '[' '+' ']'"
    p[0] = infix_function_pairs[p[2]]

def p_primaryvar16(p):
    "primaryvar : '[' '-' ']'"
    p[0] = infix_function_pairs[p[2]]

def p_primaryvar17(p):
    "primaryvar : '[' '*' ']'"
    p[0] = infix_function_pairs[p[2]]

def p_primaryvar18(p):
    "primaryvar : '[' '/' ']'"
    p[0] = infix_function_pairs[p[2]]

def p_primaryvar19(p):
    "primaryvar : '[' '^' ']'"
    p[0] = infix_function_pairs[p[2]]

def p_primaryvar20(p):
    "primaryvar : '[' '%' ']'"
    p[0] = infix_function_pairs[p[2]]

def p_primaryvar21(p):
    "primaryvar : '[' DIV ']'"
    p[0] = infix_function_pairs[p[2]]

def p_primaryvar22(p):
    "primaryvar : '(' conditional ')'"
    p[0] = p[2]

def p_error(p):
    print("ERRO NA GERACAO DE CODIGO")

test = '''
"""fpy
fdef [<>](_,[]) { [] }
fdef [<>](f,[h|t]) {
        [ f(h) | f <> t ]
}
"""
'''

def gen_code(code: str):
    parser = yacc.yacc()
    p = parser.parse(code)
    return p

# testing
# if __name__ == "__main__":
#     # code = sys.stdin.read()
#     print(gen_code(test))