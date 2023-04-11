from ply import yacc
from lexer import tokens
import semantics as sem

code_: sem.code = sem.code()
scope = []


def p_empty(p):
    'empty : '
    pass


def p_scope(p):
    'scope : '
    scope.append(set())


def p_func(p):
    'func : FDEF ID LPAR scope args RPAR LBRACE body RBRACE'
    sem.code.insert_func(sem.func(name=p[2], args=p[5], body=p[8]))
    scope.pop()


def p_lvar_var(p):
    '''lvar : var
            | llist
            | ltuple'''
    p[0] = p[1]


def p_llist(p):
    'llist : LBRACKET llist_cont'
    p[0] = p[1]


def p_llist_cont_empty(p):
    'llist_cont : RBRACKET'
    p[0] = sem.llist(type='llist')


def p_llist_term_lvar(p):
    'llist_term : lvar'
    try:
        p[0].add_lvar(p[1])
    except:
        p[0] = sem.llist(type='llist')
        p[0].add_lvar(p[1])


def p_llist_term_COMMA_LISTER(p):
    '''llist_term : llist_term COMMA lvar
                  | lvar LISTER llist'''
    try:
        p[1].add_lvar(p[3])
        p[0] = p[1]
    except:
        p[1] = sem.llist(type='llist', llist_term=p[3])
        p[0] = p[1]


def p_ltuple_LPAR(p):
    'ltuple : LPAR ltuple_cont'
    p[0] = p[2]


def p_ltuple_cont_empty(p):
    'ltuple_cont : empty RPAR'
    p[0] = sem.ltuple(type='ltuple')


def p_ltuple_cont_lvar(p):
    'ltuple_cont : ltuple_term COMMA lvar RPAR'
    p[0] = p[1].add_lvar(p[3])


def p_ltuple_term_lvar(p):
    'ltuple_term : lvar'
    try:
        p[0].add_lvar(p[1])
    except:
        p[0] = sem.ltuple(type='ltuple', ltuple_term=p[1])
        p[0].add_lvar(p[1])


def p_ltuple_term_cont(p):
    'ltuple_term : ltuple_term COMMA lvar'
    try:
        p[1].add_lvar(p[1])
        p[0] = p[1]
    except:
        p[1] = sem.ltuple(type='ltuple', ltuple_term=p[1])
        p[1].add_lvar(p[1])
        p[0] = p[1]


def p_body_statement(p):
    'body : statement body'
    try:
        p[0].statements.append(p[1])
    except:
        p[0] = sem.body('statement_body', p[1])
        p[0].statements.append(p[1])


def p_body_exp(p):
    'body : exp'
    try:
        p[0] = sem.body('body', p[1])
    except:
        print('''Found statement, expected expression at the end of function.
        Accepted types are: ''')


def p_statement(p):
    '''statement : assign
                 | reassign'''
    p[0] = p[1]


def p_assign_reassign(p):
    '''assign : lvar ASSIGN exp
              | lvar REASSIGN exp'''
    type = 'reassign' if p[2] == '=' else 'assign'
    p[0] = sem.statement(type=type, lvar=p[1], exp=p[3])


def p_exp(p):
    '''exp : rvar
           | eval
           | aritm
           | cond
           | lambda'''
    p[0] = p[1]


def p_lambda_(p):
    'lambda : LAMBDA args LBRACE exp RBRACE'
    p[0] = sem.lambda_(type='lambda', args=p[2], exp=p[4])


def p_cond(p):
    'COND LBRACE condition RBRACE'
    p[0] = p[1]


def p_cond_if_then_else(p):
    'cond : IF eval THEN exp ELSE exp'
    p[0] = sem.if_then_else(type='if_then_else',
                            eval=p[2], then=p[4], else_=p[6])


def p_condition(p):
    'condition : condition_cont ELSE COLON exp'
    p[0].add_condition(p[1])
    p[0].add_condition(p[4])


def p_condition_cont_evalexp(p):
    'condition_cont : evalexp'
    try:
        p[0].add_condition(p[1])
    except:
        p[0] = sem.cond('cond')
        p[0].add_condition(p[1])


def p_condition_cont_evalexp(p):
    'condition_cont : evalexp COMMA condition_cont'
    try:
        p[0].add_condition(p[1])
    except:
        p[0] = sem.cond('cond')
        p[0].add_condition(p[1])


def p_evalexp(p):
    'evalexp : eval COLON exp'
    p[0] = (p[1], p[3])


def p_eval_ID(p):
    'eval : ID'
    p[0] = p[1]


def p_eval_exp_OP_eval(p):
    '''eval : exp EQ eval
            | exp DIF eval
            | exp LT eval
            | exp GT eval
            | exp LTE eval
            | exp GTE eval'''
    print(p[2])
    p[0] = sem.eval(type='eval', condition=(p[2], p[1], p[3]))


def p_eval_PAR(p):
    'eval : LPAR eval RPAR'
    p[0] = p[2]


def p_aritm_ID_NUM(p):
    '''aritm : ID
             | NUM'''
    p[0] = p[1]


def p_aritm_OP(p):
    '''aritm : ID SUM aritm
             | ID PROD aritm
             | ID DIV aritm
             | ID SUB aritm
             | ID MOD aritm
             | ID POW aritm
             | ID INTDIV aritm
             | ID SUM aritm
             | NUM PROD aritm
             | NUM DIV aritm
             | NUM SUB aritm
             | NUM MOD aritm
             | NUM POW aritm
             | NUM INTDIV aritm'''
    p[0] = sem.aritm(
        type='aritm',
        op=p[2],
        var=p[1],
        aritm=p[3])


def p_aritm_aritm(p):
    'aritm : LPAR aritm RPAR'
    p[0] = p[2]


def p_rvar(p):
    '''rvar : var
            | rlist
            | rtuple
            | func_call'''
    p[0] = p[1]


def p_rlist(p):
    'rlist : LBRACKET rlist_cont'
    p[0] = p[2]


def p_rlist_cont(p):
    'rlist_cont : RBRACKET'
    pass


def p_rlist_cont_term(p):
    'rlist_cont : rlist_term RBRACKET'
    p[0] = p[1]


def p_rlist_term_exp(p):
    'rlist_term : exp'
    try:
        p[0].add_exp(p[1])
    except:
        p[0] = sem.rlist(type='llist')
        p[0].add_exp(p[1])


def p_rlist_term_COMMA_LISTER(p):
    '''llist_term : llist_term COMMA lvar
                  | lvar LISTER llist'''
    try:
        p[1].add_lvar(p[3])
        p[0] = p[1]
    except:
        p[1] = sem.llist(type='llist', llist_term=p[3])
        p[0] = p[1]


def p_rtuple_LPAR(p):
    'rtuple : LPAR rtuple_cont'
    p[0] = p[2]


def p_rtuple_cont_empty(p):
    'rtuple_cont : empty RPAR'
    p[0] = sem.rtuple(type='rtuple')


def p_rtuple_cont_exp(p):
    'rtuple_cont : rtuple_term COMMA exp RPAR'
    p[0] = p[1].add_exp(p[3])


def p_rtuple_term_epx(p):
    'rtuple_term : exp'
    try:
        p[0].add_exp(p[1])
    except:
        p[0] = sem.rtuple(type='rtuple', rtuple_term=p[1])
        p[0].add_exp(p[1])


def p_rtuple_term_cont(p):
    'rtuple_term : rtuple_term COMMA exp'
    try:
        p[1].add_exp(p[1])
        p[0] = p[1]
    except:
        p[1] = sem.rtuple(type='rtuple', rtuple_term=p[1])
        p[1].add_exp(p[1])
        p[0] = p[1]


def p_func_call(p):
    'func_call : ID LPAR func_call_cont'
    p[3].add_id(p[1])
    p[0] = p[3]


def p_func_call_cont_RPAR(p):
    'func_call_cont : RPAR'
    pass


def p_func_call_cont_COMMA(p):
    'func_call_cont : exp COMMA func_call_cont'
    try:
        p[0].add_args(p[1])
    except:
        p[0] = sem.func_call(type='func_call')
        p[0].add_args(p[1])


def p_var(p):
    '''var : ID
           | NUM
           | STRING
           | CHAR'''
    p[0] = sem.var(
        type=p[1].token().type,
        var=p[1])


def p_error(p):
    if not p:
        pass
    # obviamente, erros provisórios
    print('Deu erro')
    while True:
        tok = syntaxer.token()
        if not tok or tok.type == 'RBRACE':
            break
    syntaxer.restart()


def start_syntaxer():
    global syntaxer
    syntaxer = yacc.yacc()


if __name__ == '__main__':
    start_syntaxer()
