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
    "function : scope conditional '}'"

def p_scope(p):
    "scope : main_scope"

def p_scope1(p):
    "scope : main_scope let_block"

def p_main_scope(p):
    "main_scope : new_f args returntype '{'"

def p_new_f(p):
    "new_f : FDEF prefix"

def p_args(p):
    "args : '(' ')'"

def p_args1(p):
    "args : '(' arg_list ')'"

def p_lpattern_scope(p):
    "lpattern_scope : "

def p_arg_list(p):
    "arg_list : lpattern_scope lpattern annotation"

def p_arg_list1(p):
    "arg_list : arg_list ',' lpattern_scope lpattern annotation"

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
    "typeclass : ID ID"

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
    "lvar : STRINGT"

def p_lvar2(p):
    "lvar : INTT"

def p_lvar3(p):
    "lvar : FLOATT"

def p_lvar4(p):
    "lvar : CHART"

def p_lvar5(p):
    "lvar : BOOLT"

def p_lvar6(p):
    "lvar : '[' SPECIALID ']'"

def p_lvar7(p):
    "lvar : '[' OR ']'"

def p_lvar8(p):
    "lvar : '[' AND ']'"

def p_lvar9(p):
    "lvar : '[' EQ ']'"

def p_lvar10(p):
    "lvar : '[' NEQ ']'"

def p_lvar11(p):
    "lvar : '[' '>' ']'"

def p_lvar12(p):
    "lvar : '[' '<' ']'"

def p_lvar13(p):
    "lvar : '[' GTE ']'"

def p_lvar14(p):
    "lvar : '[' LTE ']'"

def p_lvar15(p):
    "lvar : '[' '+' ']'"

def p_lvar16(p):
    "lvar : '[' '-' ']'"

def p_lvar17(p):
    "lvar : '[' '*' ']'"

def p_lvar18(p):
    "lvar : '[' '/' ']'"

def p_lvar19(p):
    "lvar : '[' '^' ']'"

def p_lvar20(p):
    "lvar : '[' '%' ']'"

def p_lvar21(p):
    "lvar : '[' DIV ']'"

def p_lvar22(p):
    "lvar : '(' lpattern ')'"

def p_conditional(p):
    "conditional : UNDEFINED"

def p_conditional1(p):
    "conditional : compound"

def p_conditional2(p):
    "conditional : IF conditional THEN conditional ELSE conditional"

def p_compound(p):
    "compound : compound OR or_exp"

def p_compound1(p):
    "compound : or_exp"

def p_compound2(p):
    "compound : '[' compound OR ']'"

def p_compound3(p):
    "compound : '[' OR or_exp ']'"

def p_or_exp(p):
    "or_exp : or_exp AND relat"

def p_or_exp1(p):
    "or_exp : relat"

def p_or_exp2(p):
    "or_exp : '[' or_exp AND ']'"

def p_or_exp3(p):
    "or_exp : '[' AND relat ']'"

def p_relat(p):
    "relat : relat relat_op aritm"

def p_relat1(p):
    "relat : aritm"

def p_relat2(p):
    "relat : '[' relat relat_op ']'"

def p_relat3(p):
    "relat : '[' relat_op aritm ']'"

def p_relat_op(p):
    "relat_op : EQ"

def p_relat_op1(p):
    "relat_op : NEQ"

def p_relat_op2(p):
    "relat_op : '>'"

def p_relat_op3(p):
    "relat_op : '<'"

def p_relat_op4(p):
    "relat_op : GTE"

def p_relat_op5(p):
    "relat_op : LTE"

def p_aritm(p):
    "aritm : aritm aritm_op factor"

def p_aritm1(p):
    "aritm : factor"

def p_aritm2(p):
    "aritm : '[' aritm aritm_op ']'"

def p_aritm3(p):
    "aritm : '[' aritm_op factor ']'"

def p_aritm_op(p):
    "aritm_op : '+'"

def p_aritm_op1(p):
    "aritm_op : '-'"

def p_factor(p):
    "factor : factor factor_op pow"

def p_factor1(p):
    "factor : pow"

def p_factor2(p):
    "factor : '[' factor factor_op ']'"

def p_factor3(p):
    "factor : '[' factor_op pow ']'                    "

def p_factor_op(p):
    "factor_op : '*'"

def p_factor_op1(p):
    "factor_op : '/'"

def p_factor_op2(p):
    "factor_op : '%'"

def p_factor_op3(p):
    "factor_op : DIV"

def p_pow(p):
    "pow : pow '^' rest"

def p_pow1(p):
    "pow : rest"

def p_pow2(p):
    "pow : '[' pow '^' ']'"

def p_pow3(p):
    "pow : '[' '^' rest ']'"

def p_rest(p):
    "rest : rest infix single"

def p_rest1(p):
    "rest : single"

def p_rest2(p):
    "rest : '[' infix single ']'"

def p_rest3(p):
    "rest : '[' rest infix ']'"

def p_infix(p):
    "infix : '`' ID '`'"

def p_infix1(p):
    "infix : SPECIALID"

def p_single(p):
    "single : multivar"

def p_single1(p):
    "single : lambda"

def p_single2(p):
    "single : cond_block"

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
    "lambda : FDEF '(' lambda_scope pattern_list ')' '{' conditional '}'"

def p_lambda_scope(p):
    "lambda_scope : "

def p_multivar(p):
    "multivar : multivar '(' ')'"

def p_multivar1(p):
    "multivar : multivar '(' condition_list ')'"

def p_multivar2(p):
    "multivar : rlist"

def p_multivar3(p):
    "multivar : rtuple"

def p_multivar4(p):
    "multivar : primaryvar"

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

def p_rtuple(p):
    "rtuple : '(' ')'"

def p_rtuple1(p):
    "rtuple : '(' rtuple_cont ')'"

def p_rtuple_cont(p):
    "rtuple_cont : conditional ',' conditional"

def p_rtuple_cont1(p):
    "rtuple_cont : rtuple_cont ',' conditional"

def p_primaryvar(p):
    "primaryvar : ID"

def p_primaryvar1(p):
    "primaryvar : INTT"

def p_primaryvar2(p):
    "primaryvar : FLOATT"

def p_primaryvar3(p):
    "primaryvar : CHART"

def p_primaryvar4(p):
    "primaryvar : STRINGT"

def p_primaryvar5(p):
    "primaryvar : BOOLT"

def p_primaryvar6(p):
    "primaryvar : '[' SPECIALID ']'"

def p_primaryvar7(p):
    "primaryvar : '[' OR ']'"

def p_primaryvar8(p):
    "primaryvar : '[' AND ']'"

def p_primaryvar9(p):
    "primaryvar : '[' EQ ']'"

def p_primaryvar10(p):
    "primaryvar : '[' NEQ ']'"

def p_primaryvar11(p):
    "primaryvar : '[' '>' ']'"

def p_primaryvar12(p):
    "primaryvar : '[' '<' ']'"

def p_primaryvar13(p):
    "primaryvar : '[' GTE ']'"

def p_primaryvar14(p):
    "primaryvar : '[' LTE ']'"

def p_primaryvar15(p):
    "primaryvar : '[' '+' ']'"

def p_primaryvar16(p):
    "primaryvar : '[' '-' ']'"

def p_primaryvar17(p):
    "primaryvar : '[' '*' ']'"

def p_primaryvar18(p):
    "primaryvar : '[' '/' ']'"

def p_primaryvar19(p):
    "primaryvar : '[' '^' ']'"

def p_primaryvar20(p):
    "primaryvar : '[' '%' ']'"

def p_primaryvar21(p):
    "primaryvar : '[' DIV ']'"

def p_primaryvar22(p):
    "primaryvar : '(' conditional ')'"

parser = yacc.yacc()
