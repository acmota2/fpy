import ply.yacc as yacc
import ply.lex as lex
from lexer import tokens, literals
import sys

def p_grammar_tester(p):
    '''
    all             : 
                    | BEGIN END
                    | BEGIN body END

    body            : statement
                    | body statement

    statement       : function
                    | ALIAS ID '=' typedesc
                    | LET ID annotation '=' conditional

    function        : FDEF prefix args returntype '{' compound '}'
                    | FDEF prefix args returntype '{' let_block compound '}'

    args            : '(' ')'
                    | '(' arg_list ')'

    arg_list        : lpattern annotation
                    | arg_list ',' lpattern annotation

    prefix          : ID
                    | '[' SPECIALID ']'

    returntype      : 
                    | RARROW typedesc

    let_block       : LET '{' let_cont '}'

    let_cont        : assign
                    | let_cont ',' assign

    assign          : lpattern annotation '=' conditional

    lpattern        : lvar
                    | llist
                    | ltuple

    annotation      : 
                    | ':' typedesc

    typedesc        : typeid
                    | typeclass
                    | function_type
                    | '(' tuple_type ')'

    typeclass       : TYPECLASS ID

    function_type   : '(' typedesc ')' RARROW typedesc
                    | '(' tuple_type ')' RARROW typedesc

    tuple_type      : typeid ',' typeid
                    | tuple_type ',' typeid

    typeid          : INT
                    | FLOAT
                    | CHAR
                    | BOOL
                    | ID
                    | '[' typedesc ']'

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
                    | STRINGT
                    | INTT
                    | FLOATT
                    | CHART
                    | BOOLT
                    | '(' lpattern ')'

    conditional     : compound
                    | IF conditional THEN conditional ELSE conditional

    compound        : expression
                    | compound infix expression
                    | '(' compound infix ')'
                    | '(' infix expression ')'

    infix           : '`' ID '`'
                    | SPECIALID

    expression      : multivar
                    | lambda
                    | cond_block

    cond_block      : COND '{' cond ',' ELSE ':' conditional '}'

    cond            : cond_singl
                    | cond ',' cond_singl

    cond_singl      : conditional ':' conditional

    lambda          : FDEF '(' ')' '{' conditional '}' 
                    | FDEF '(' pattern_list ')' '{' conditional '}'

    multivar        : primaryvar
                    | rlist
                    | rtuple
                    | multivar '(' condition_list ')'

    primaryvar      : ID
                    | '[' SPECIALID ']'
                    | INTT
                    | FLOATT
                    | CHART
                    | BOOLT
                    | '(' conditional ')'

    rtuple          : '(' ')'
                    | '(' rtuple_cont ')'

    rtuple_cont     : conditional ',' conditional
                    | rtuple_cont ',' conditional

    rlist           : '[' ']'
                    | '[' condition_list ']'
                    | '[' conditional '|' conditional ']'
                    | '[' conditional RANGER conditional ']'

    condition_list  : conditional
                    | condition_list ',' conditional
    '''


def p_error(p):
    if not p:
        pass
    # obviamente, erros provisórios
    print(f"Deu erro em '{p}' on line {p.lexer.lineno}")
    while True:
        tok = parser.token()
        if not tok or tok.type == 'RBRACE':
            break
    parser.restart()

data = sys.stdin.read()

parser = yacc.yacc(debug=True)
parser.parse(data)
