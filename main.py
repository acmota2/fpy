'''
SIMPLIFIED GRAMMAR

code            : func
                | code func
func            : FDEF ID args LBRACE body RBRACE

args            : LPAR args_cont
args_cont       : RPAR
                | args_cont COMMA lvar
                | lvar

lvar            : singl
                | llist
                | ltuple

llist           : LBRACKET llist_cont
llist_cont      : RBRACKET
                | llist_term RBRACKET
llist_term      : singl
                | list_term COMMA singl
                | singl LISTER llist

ltuple          : LPAR
                | ltuple_cont RPAR
ltuple_cont     : lvar
                | ltuple_cont COMMA singl

body            : exp
                | statement body

statement       : lvar ASSIGN exp
                | lvar REASSIGN exp

exp             : rvar
                | eval
                | aritm
                | cond
                | lambda

lambda          : LAMBDA args LBRACE exp RBRACE
                | LAMBDA args LBRACE cond RBRACE

cond            : COND LBRACE condition RBRACE
                | IF eval THEN exp ELSE exp

condition       : condition_cont '_' COLON exp

condition_cont  : evalexp
                | evalexp COMMA condition_cont

evalexp         : eval COLON exp

eval            : ID
                | eval 'cond_op' aritm
                | LPAR eval RPAR

aritm           : ID
                | NUM
                | ID 'aritm_op' aritm
                | NUM 'aritm_op' aritm
                | LPAR aritm RPAR

rvar            : singl
                | rlist
                | rtuple
                | func_call

rlist           : LBRACKET rlist_cont
rlist_cont      : RBRACKET
                | rlist_term RBRACKET
rlist_term      : exp
                | rlist_term COMMA exp
                | exp LISTER rlist

rtuple          : LPAR
                | rtuple_cont COMMA exp RPAR
rtuple_cont     : exp
                | rtuple_cont COMMA exp

func_call       : ID LPAR func_call_cont
func_call_cont  : RPAR
                | exp COMMA func_call_cont

singl           : ID
                | NUM
                | STRING
                | CHAR
'''

if __name__ == '__main__':
    ...