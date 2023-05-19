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
    all             : BEGIN body END

    body            : function
                    | body function

    function        : FDEF prefix args '{' compound '}'
                    | FDEF prefix args '{' let_block compound '}'

    args            : '(' ')'
                    | '(' pattern_list ')'

    prefix          : ID
                    | '[' SPECIALID ']'

    let_block       : LET '{' let_cont '}'

    let_cont        : assign
                    | let_cont ',' assign

    assign          : lpattern '=' compound

    lpattern        : lvar
                    | llist
                    | ltuple

    llist           : '[' ']'
                    | '[' pattern_list ']'
                    | '[' lpattern '|' lpattern ']'

    pattern_list    : lpattern
                    | pattern_list ',' lpattern

    ltuple          : '(' ')'
                    | '(' ltuple_cont ')'

    ltuple_cont     : lpattern ',' lpattern
                    | ltuple_cont ',' lpattern

    lvar            : ID
                    | '[' SPECIALID ']'
                    | STRING
                    | NUM
                    | CHAR
                    | BOOL
                    | '(' lpattern ')'

    compound        : expression
                    | compound infix expression
                    | '(' infix expression ')'
                    | '(' expression infix ')'

    infix           : '`' ID '`'
                    | SPECIALID

    expression      : multivar
                    | lambda
                    | conditional

    lambda          : FDEF '(' ')' '{' expression '}' 
                    | FDEF '(' pattern_list ')' '{' expression '}'

    conditional     : COND '{' cond ',' ELSE ':' expression '}'
                    | IF expression THEN expression ELSE expression

    cond            : cond_singl
                    | cond ',' cond_singl

    cond_singl      : expression ':' expression

    multivar        : primaryvar
                    | rlist
                    | rtuple
                    | multivar '(' compound_list ')'

    compound_list   : compound
                    | compound_list ',' compound

    primaryvar      : ID
                    | '[' SPECIALID ']'
                    | STRING
                    | NUM
                    | CHAR
                    | BOOL
                    | '(' expression ')'

    rtuple          : '(' ')'
                    | '(' rtuple_cont ')'

    rtuple_cont     : expression ',' expression
                    | rtuple_cont ',' expression

    rlist           : '[' ']'
                    | '[' exp_list ']'
                    | '[' expression '|' expression ']'
                    | '[' expression RANGER expression ']'

    exp_list        : expression
                    | exp_list ',' expression
    '''
    print('Worked!')


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
