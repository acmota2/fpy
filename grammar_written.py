from lexer import tokens, literals
import ply.yacc as yacc

def p_all(p):
    "all : "

def p_all1(p):
    "all : BEGIN END"

def p_all2(p):
    "all : BEGIN body END"

def p_body(p):
    "body : statement"

def p_body1(p):
    "body : body statement"

def p_statement(p):
    "statement : function"

def p_statement1(p):
    "statement : ALIAS ID '=' typedesc"

def p_statement2(p):
    "statement : LET ID annotation '=' conditional"

def p_function(p):
    "function : FDEF prefix args returntype '{' compound '}'"

def p_function1(p):
    "function : FDEF prefix args returntype '{' let_block compound '}'"

def p_args(p):
    "args : '(' ')'"

def p_args1(p):
    "args : '(' arg_list ')'"

def p_arg_list(p):
    "arg_list : lpattern annotation"

def p_arg_list1(p):
    "arg_list : arg_list ',' lpattern annotation"

def p_prefix(p):
    "prefix : ID"

def p_prefix1(p):
    "prefix : '[' SPECIALID ']'"

def p_returntype(p):
    "returntype : "

def p_returntype1(p):
    "returntype : RARROW typedesc"

def p_annotation(p):
    "annotation : "

def p_annotation1(p):
    "annotation : ':' typedesc"

def p_typedesc(p):
    "typedesc : typeid"

def p_typedesc1(p):
    "typedesc : typeclass"

def p_typedesc2(p):
    "typedesc : function_type"

def p_typedesc3(p):
    "typedesc : '(' tuple_type ')'"

def p_typeclass(p):
    "typeclass : TYPECLASS ID"

def p_function_type(p):
    "function_type : '(' typedesc ')' RARROW typedesc"

def p_function_type1(p):
    "function_type : '(' tuple_type ')' RARROW typedesc"

def p_tuple_type(p):
    "tuple_type : typeid ',' typeid"

def p_tuple_type1(p):
    "tuple_type : tuple_type ',' typeid"

def p_typeid(p):
    "typeid : INT"

def p_typeid1(p):
    "typeid : FLOAT"

def p_typeid2(p):
    "typeid : CHAR"

def p_typeid3(p):
    "typeid : BOOL"

def p_typeid4(p):
    "typeid : ID"

def p_typeid5(p):
    "typeid : '[' typedesc ']'"

def p_let_block(p):
    "let_block : LET '{' let_cont '}'"

def p_let_cont(p):
    "let_cont : assign"

def p_let_cont1(p):
    "let_cont : let_cont ',' assign"

def p_assign(p):
    "assign : lpattern annotation '=' conditional"

def p_lpattern(p):
    "lpattern : lvar"

def p_lpattern1(p):
    "lpattern : llist"

def p_lpattern2(p):
    "lpattern : ltuple"

def p_llist(p):
    "llist : '[' ']'"

def p_llist1(p):
    "llist : '[' pattern_list ']'"

def p_llist2(p):
    "llist : '[' lpattern '|' lpattern ']'"

def p_pattern_list(p):
    "pattern_list : lpattern"

def p_pattern_list1(p):
    "pattern_list : pattern_list ',' lpattern"

def p_ltuple(p):
    "ltuple : '(' ')'"

def p_ltuple1(p):
    "ltuple : '(' ltuple_cont ')'"

def p_ltuple_cont(p):
    "ltuple_cont : lpattern ',' lpattern"

def p_ltuple_cont1(p):
    "ltuple_cont : ltuple_cont ',' lpattern"

def p_lvar(p):
    "lvar : ID"

def p_lvar1(p):
    "lvar : '[' SPECIALID ']'"

def p_lvar2(p):
    "lvar : STRINGT"

def p_lvar3(p):
    "lvar : INTT"

def p_lvar4(p):
    "lvar : FLOATT"

def p_lvar5(p):
    "lvar : CHART"

def p_lvar6(p):
    "lvar : BOOLT"

def p_lvar7(p):
    "lvar : '(' lpattern ')'"

def p_conditional(p):
    "conditional : compound"

def p_conditional1(p):
    "conditional : IF conditional THEN conditional ELSE conditional"

def p_compound(p):
    "compound : expression"

def p_compound1(p):
    "compound : compound infix expression"

def p_compound2(p):
    "compound : '(' compound infix ')'"

def p_compound3(p):
    "compound : '(' infix expression ')'"

def p_infix(p):
    "infix : '`' ID '`'"

def p_infix1(p):
    "infix : SPECIALID"

def p_expression(p):
    "expression : multivar"

def p_expression1(p):
    "expression : lambda"

def p_expression2(p):
    "expression : cond_block"

def p_cond_block(p):
    "cond_block : COND '{' cond ',' ELSE ':' conditional '}'"

def p_cond(p):
    "cond : cond_singl"

def p_cond1(p):
    "cond : cond ',' cond_singl"

def p_cond_singl(p):
    "cond_singl : conditional ':' conditional"

def p_lambda(p):
    "lambda : FDEF '(' ')' '{' conditional '}' "

def p_lambda1(p):
    "lambda : FDEF '(' pattern_list ')' '{' conditional '}'"

def p_multivar(p):
    "multivar : primaryvar"

def p_multivar1(p):
    "multivar : rlist"

def p_multivar2(p):
    "multivar : rtuple"

def p_multivar3(p):
    "multivar : multivar '(' condition_list ')'"

def p_primaryvar(p):
    "primaryvar : ID"

def p_primaryvar1(p):
    "primaryvar : '[' SPECIALID ']'"

def p_primaryvar2(p):
    "primaryvar : INTT"

def p_primaryvar3(p):
    "primaryvar : FLOATT"

def p_primaryvar4(p):
    "primaryvar : CHART"

def p_primaryvar5(p):
    "primaryvar : BOOLT"

def p_primaryvar6(p):
    "primaryvar : '(' conditional ')'"

def p_rtuple(p):
    "rtuple : '(' ')'"

def p_rtuple1(p):
    "rtuple : '(' rtuple_cont ')'"

def p_rtuple_cont(p):
    "rtuple_cont : conditional ',' conditional"

def p_rtuple_cont1(p):
    "rtuple_cont : rtuple_cont ',' conditional"

def p_rlist(p):
    "rlist : '[' ']'"

def p_rlist1(p):
    "rlist : '[' condition_list ']'"

def p_rlist2(p):
    "rlist : '[' conditional '|' conditional ']'"

def p_rlist3(p):
    "rlist : '[' conditional RANGER conditional ']'"

def p_condition_list(p):
    "condition_list : conditional"

def p_condition_list1(p):
    "condition_list : condition_list ',' conditional"

parser = yacc.yacc()
