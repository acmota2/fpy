from syntax import code
from .ply import yacc
from lexer import tokens

code = code()

# def p_code_func(p):
#     'code : func'
#     p[0] = p[1]

# def p_code_code_func(p):
#     'code : code func'
#     p[0] = f'{p[1]}\n{p[2]}'

def p_body_statement(p):
    'body : statement body'
    p[0] = f'{p[1]}\n'

def p_body_exp(p):
    'body : exp'
    p[0] = p[1]

def p_statement_REASSIGN(p):
    'statement : lvar REASSIGN exp'
    p[0] = f'{p[1]}={p[3]}'

def p_statement_ASSIGN(p):
    'statement : lvar ASSIGN exp'
    p[0] = f'{p[1]}={p[3]}'

def p_exp_cond(p):
    'exp : cond'
    p[0] = p[1]

def p_exp_aritm(p):
    'exp : aritm'
    p[0] = p[1]

def p_exp_eval(p):
    'exp : eval'
    p[0] = p[1]

def p_exp_rvar(p):
    'exp : rvar'
    p[0] = p[1]

def p_cond_condition(p):
    'cond : COND LBRACE condition RBRACE'
    p[0] = p[3]

def p_cond_IF_THEN_ELSE(p):
    'cond : IF eval THEN exp ELSE exp'
    p[0] = f'{p[4]} if {p[2]} else {p[6]}'

def p_condition_IF_ELIF(p):
    'condition : evalexp COMMA condition'
    p[0] = f"""
    {p[1]}
    el{p[3]}
    """

def p_condition_IF_ELSE(p):
    "condition : evalexp COMMA '_' COLON exp"
    p[0] = f"""
    {p[1]}
    else:
        {p[7]}
    """

def p_evalexp(p):
    'evalexp : eval COLON exp'
    p[0] = f'''
    if {p[1]}:
        {p[3]}
    '''

def p_eval_DIF(p):
    'eval : eval DIF aritm'
    p[0] = f'{p[1]}!={p[3]}'

def p_eval_GTE(p):
    'eval : eval GTE aritm'
    p[0] = f'{p[1]}>={p[3]}'

def p_eval_LTE(p):
    'eval : eval LTE aritm'
    p[0] = f'{p[1]}<={p[3]}'

def p_eval_GT(p):
    'eval : eval GT aritm'
    p[0] = f'{p[1]}>{p[3]}'

def p_eval_LT(p):
    'eval : eval LT aritm'
    p[0] = f'{p[1]}<{p[3]}'

def p_eval_EQ(p):
    'eval : eval EQ aritm'
    p[0] = f'{p[1]}=={p[3]}'

def p_eval_PARS(p):
    'eval : LPAR eval RPAR'
    p[0] = f'({p[2]})'

def p_eval_ID(p):
    'eval : ID'
    p[0] = p[1]

def p_aritm_NUM_MOD(p):
    'aritm : NUM MOD aritm'
    p[0] = f'{p[1]}%{p[3]}'

def p_aritm_NUM_POW(p):
    'aritm : NUM POW aritm'
    p[0] = f'{p[1]}**{p[2]}'

def p_aritm_NUM_INTDIV(p):
    'aritm : NUM DIV aritm'
    p[0] = f'{p[1]}//{p[3]}'

def p_aritm_NUM_PROD(p):
    'aritm : NUM PROM aritm'
    p[0] = rf'{p[1]}*{p[3]}'

def p_aritm_NUM_DIV(p):
    'aritm : NUM SUB aritm'
    p[0] = f'{p[1]}/{p[3]}'

def p_aritm_NUM_SUB(p):
    'aritm : NUM SUB aritm'
    p[0] = f'{p[1]}-{p[3]}'

def p_aritm_NUM_SUM(p):
    'aritm : NUM SUM aritm'
    p[0] = f'{p[1]}+{p[3]}'

def p_aritm_ID_MOD(p):
    'aritm : ID MOD aritm'
    p[0] = f'{p[1]}%{p[3]}'

def p_aritm_ID_POW(p):
    'aritm : ID POW aritm'
    p[0] = f'{p[1]}**{p[2]}'

def p_aritm_ID_INTDIV(p):
    'aritm : ID DIV aritm'
    p[0] = f'{p[1]}//{p[3]}'

def p_aritm_ID_PROD(p):
    'aritm : ID PROM aritm'
    p[0] = rf'{p[1]}*{p[3]}'

def p_aritm_ID_DIV(p):
    'aritm : ID SUB aritm'
    p[0] = f'{p[1]}/{p[3]}'

def p_aritm_ID_SUB(p):
    'aritm : ID SUB aritm'
    p[0] = f'{p[1]}-{p[3]}'

def p_aritm_ID_SUM(p):
    'aritm : ID SUM aritm'
    p[0] = f'{p[1]}+{p[3]}'

def p_aritm_NUM(p):
    'aritm : NUM'
    p[0] = p[1]

def p_aritm_ID(p):
    'aritm : ID'
    p[0] = p[1]

def p_aritm_LPAR_RPAR(p):
    'aritm : LPAR aritm RPAR'
    p[0] = f'({p[2]})'

def p_rvar_rtuple(p):
    'rvar : rtuple'
    p[0] = p[1]

def p_rvar_rlist(p):
    'rvar : rlist'
    p[0] = p[1]

def p_rvar_singl(p):
    'rvar : singl'
    p[0] = p[1]

def p_rlist_LBRACKET(p):
    'rlist : LBRACKET'
    p[0] = '['

def p_rlist_cont_RBRACKET(p):
    'rlist_cont : RBRACKET'
    p[0] = ']'

def p_rlist_cont_LBRACKET(p):
    'rlist_term : rlist_term RBRACKET'
    p[0] = f'{p[1]}]'

def p_rtuple_LPAR(p):
    'rtuple : LPAR'
    p[0] = '('

def p_rtuple_RPAR(p):
    'rtuple : rtuple_cont RPAR'
    p[0] = f'{p[1]})'

def p_rtuple_cont_exp(p):
    'rtuple_cont : exp'
    p[0] = p[1]

def p_rtuple_cont_COMMA(p):
    'rtuple_cont : rtuple_cont COMMA exp'
    p[0] = f'({p[1]},{p[3]})'

def p_singl_ID(p):
    'singl : ID'
    p[0] = p[1]

def p_singl_NUM(p):
    'singl : NUM'
    p[0] = p[1]

def p_singl_STRING(p):
    'singl : STRING'
    p[0] = p[1]

def p_singl_CHAR(p):
    'singl : CHAR'
    p[0] = p[1]
