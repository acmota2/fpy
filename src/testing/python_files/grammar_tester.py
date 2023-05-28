import ply.yacc as yacc
import ply.lex as lex
from lexer_tester import tokens, literals
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

    function        : scope conditional '}'

    scope           : main_scope
                    | main_scope let_block

    main_scope      : new_f args returntype '{'

    new_f           : FDEF prefix

    args            : '(' ')'
                    | '(' arg_list ')'

    lpattern_scope  :

    arg_list        : lpattern_scope lpattern annotation
                    | arg_list ',' lpattern_scope lpattern annotation

    prefix          : ID
                    | '[' SPECIALID ']'

    returntype      : 
                    | RARROW typedesc

    annotation      : 
                    | ':' typedesc

    typedesc        : typeid
                    | typeclass
                    | function_type
                    | '(' tuple_type ')'

    typeclass       : ID ID

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

    let_block       : LET '{' let_cont '}'

    let_cont        : assign
                    | let_cont ',' assign

    assign          : lpattern annotation '=' conditional

    lpattern        : lvar
                    | llist
                    | ltuple

    llist           : '[' ']'
                    |  '[' pattern_list ']'
                    |  '[' lpattern '|' lpattern ']'

    pattern_list    : lpattern
                    | pattern_list ',' lpattern

    ltuple          : '(' ')'
                    | '(' ltuple_cont ')'

    ltuple_cont     : lpattern ',' lpattern
                    | ltuple_cont ',' lpattern
                    
    lvar            : ID
                    | STRINGT
                    | INTT
                    | FLOATT
                    | CHART
                    | BOOLT
                    | '[' SPECIALID ']'
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
                    | '[' DIV ']'
                    | '(' lpattern ')'

    conditional     : UNDEFINED
                    | compound
                    | IF conditional THEN conditional ELSE conditional

    compound        : compound OR or_exp
                    | or_exp
                    | '[' compound OR ']'
                    | '[' OR or_exp ']'

    or_exp          : or_exp AND relat
                    | relat
                    | '[' or_exp AND ']'
                    | '[' AND relat ']'

    relat           : relat relat_op aritm
                    | aritm
                    | '[' relat relat_op ']'
                    | '[' relat_op aritm ']'

    relat_op        : EQ
                    | NEQ
                    | '>'
                    | '<'
                    | GTE
                    | LTE

    aritm           : aritm aritm_op factor
                    | factor
                    | '[' aritm aritm_op ']'
                    | '[' aritm_op factor ']'

    aritm_op        : '+'
                    | '-'

    factor          : factor factor_op pow
                    | pow
                    | '[' factor factor_op ']'
                    | '[' factor_op pow ']'                    

    factor_op       : '*'
                    | '/'
                    | '%'
                    | DIV

    pow             : pow '^' rest
                    | rest
                    | '[' pow '^' ']'
                    | '[' '^' rest ']'

    rest            : rest infix single
                    | single
                    | '[' infix single ']'
                    | '[' rest infix ']'

    infix           : '`' ID '`'
                    | SPECIALID

    single          : multivar
                    | lambda
                    | cond_block

    cond_block      : COND '{' cond ',' ELSE ':' conditional '}'

    cond            : cond_singl
                    | cond ',' cond_singl

    cond_singl      : conditional ':' conditional

    lambda          : FDEF '(' ')' '{' conditional '}' 
                    | FDEF '(' lambda_scope arg_list ')' '{' conditional '}'

    lambda_scope    :

    multivar        : multivar '(' ')'
                    | multivar '(' condition_list ')'
                    | rlist
                    | rtuple
                    | primaryvar

    rlist           : '[' ']'
                    | '[' condition_list ']'
                    | '[' conditional '|' conditional ']'
                    | '[' conditional RANGER conditional ']'

    condition_list  : conditional
                    | condition_list ',' conditional

    rtuple          : '(' ')'
                    | '(' rtuple_cont ')'

    rtuple_cont     : conditional ',' conditional
                    | rtuple_cont ',' conditional

    primaryvar      : ID
                    | INTT
                    | FLOATT
                    | CHART
                    | STRINGT
                    | BOOLT
                    | '[' SPECIALID ']'
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
                    | '[' DIV ']'
                    | '(' conditional ')'
    '''


def p_error(p):
    if not p:
        pass
    # obviamente, erros provisórios
    print(f"Deu erro em '{p}' on line {p.lineno}")
    while True:
        tok = parser.token()
        if not tok or tok.type == 'RBRACE':
            break
    parser.restart()

data = sys.stdin.read()

parser = yacc.yacc(debug=True)
parser.parse(data)
