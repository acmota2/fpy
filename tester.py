import ply.yacc as yacc
import ply.lex as lex
from lexer import tokens, literals
import sys

"""TESTE

'''fpy
fdef bla([]) {
	[]
}
'''

"""

def p_grammar_tester(p):
    '''
    program         : BEGIN code END

    code            : func
                    | code func

    func            : FDEF ID '(' scope ')' '{' body '}'
                    | FDEF ID '(' scope args ')' '{' body '}'

    scope           :

    args            : lvar
                    | args ',' lvar

    lvar            : multi_var
                    | llist
                    | ltuple

    llist           : '[' ']'
                    | '[' llist_cont ']'
    llist_cont      : lvar  
                    | llist_cont ',' lvar
                    | lvar '|' llist

    ltuple          : '(' ')'
                    | '(' ltuple_cont ',' lvar ')'
    ltuple_cont     : lvar
                    | ltuple_cont ',' lvar

    body            : exp
                    | statement body

    statement       : assign
                    | reassign
    assign          : lvar ASSIGN exp
    reassign        : lvar '=' exp

    exp             : rvar
                    | eval
                    | aritm
                    | cond
                    | lambda

    lambda          : '[' ']' '{' exp '}'
                    | '[' args ']' '{' exp '}'

    cond            : COND '{' condition '}'
                    | IF eval THEN exp ELSE exp
    condition       : condition_cont ELSE ':' exp
    condition_cont  : evalexp
                    | evalexp ',' condition_cont

    evalexp         : eval ':' exp

    eval            : cond_exp logic_op eval
                    | ID

    logic_op        : AND
                    | OR

    cond_exp        : exp cond_op cond_exp
                    | '(' eval ')'

    cond_op         : EQ
                    | '<'
                    | '>'
                    | LTE
                    | GTE
                    | DIF

    aritm           : ID
                    | NUM
                    | ID aritm_op aritm
                    | NUM aritm_op aritm
                    | '(' aritm ')'

    aritm_op        : '+'
                    | '-'
                    | '*'
                    | '/'
                    | '%'
                    | POW
                    | INTDIV

    rvar            : multi_var
                    | rlist
                    | rtuple
                    | func_call

    rlist           : '[' ']'
                    | '[' rlist_cont ']'
    rlist_cont      : exp
                    | rlist_cont ',' exp
                    | exp '|' rlist

    rtuple          : '(' ')'
                    | '(' rtuple_cont ',' exp ')'
    rtuple_cont     : exp
                    | rtuple_cont ',' exp

    func_call       : ID '(' ')'
                    | ID '(' func_call_cont ')'
    func_call_cont  : exp
                    | func_call_cont ',' exp

    multi_var       : ID
                    | NUM
                    | STRING
                    | CHAR
    '''


def p_error(p):
    if not p:
        pass
    # obviamente, erros provisórios
    print(f'Deu erro em {p}')
    while True:
        tok = parser.token()
        if not tok or tok.type == 'RBRACE':
            break
    parser.restart()

data = sys.stdin.read()

parser = yacc.yacc(debug=True)
parser.parse(data)
