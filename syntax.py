from syntax import code, func
from .ply import yacc
from lexer import tokens
import syntax as syn

code_: code = code()
scope = []

def p_empty(p):
    'empty : '
    pass

def p_scope(p):
    'scope : '
    scope.append(set())

def p_func(p):
    'func : FDEF ID LPAR scope args RPAR LBRACE body RBRACE'
    code.insert_func(func(name=p[2], args=p[5], body=p[8]))
    scope.pop()

def p_body_statement(p):
    'body : statement body'
    p[0] = syn.body('statement_body', p[1])

def p_body_exp(p):
    'body : exp'
    p[0] = syn.body('body', p[1])

def p_statement_REASSIGN(p):
    '''statement : assign
                 | reassign'''
    p[0] = syn.statement('reassing', p[1])

def p_lvar_var(p):
    'lvar : var'
    p[0] = syn.lvar('var', p[1])

def p_lvar_llist(p):
    'lvar : llist'
    p[0] = syn.lvar('llist', p[1])

def p_lvar_ltuple(p):
    'lvar : ltuple'
    p[0] = syn.lvar('ltuple', p[1])

def p_llist(p):
    'llist : LBRACKET llist_cont'
    p[0] = syn.llist(p[2])

def p_llist_cont_empty(p):
    'llist_cont : RBRACKET'
    pass

def p_llist_cont(p):
    'llist_cont : llist_term RBRACKET'
    p[0] = syn.llist_cont('llist_term', p[1])

def p_llist_term(p):
    'llist_term : var'
    p[0] = syn.llist_term('var', var=p[1])

def p_llist_term(p):
    'llist_term : llist_term COMMA var'
    p[0] = syn.llist_term('commas', p[1], p[3])

def p_llist_term(p):
    'llist_term : var LISTER llist'
    p[0] = syn.llist_term('lister', p[1], p[3])

def p_assign(p):
    'assign : lvar ASSIGN exp'
    # esta condição está errada, verificar!!!
    p[0] = syn.reassign_assign('assign', p[1])

def p_reassign(p):
    'assign : lvar REASSIGN exp'
    # esta condição está errada, verificar!!!
    p[0] = syn.reassign_assign('reassign', p[1])

def p_var(p):
    '''var : ID
           | NUM
           | STRING
           | CHAR'''
    p[0] = syn.var(p[1])
