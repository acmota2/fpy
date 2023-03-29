'''
GRAMMAR

empty           :

func            : FDEF ID LPAR args RPAR LBRACE body RBRACE

args            : empty
                | args COMMA lvar

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

statement       : assign
                | reassign
assign          : lvar ASSIGN exp
reassign        : lvar REASSIGN exp

exp             : rvar
                | eval
                | aritm
                | cond
                | lambda

lambda          : LAMBDA args LBRACE exp RBRACE

cond            : COND LBRACE condition RBRACE
                | IF eval THEN exp ELSE exp

condition       : condition_cont ELSE COLON exp

condition_cont  : evalexp
                | evalexp COMMA condition_cont

evalexp         : eval COLON exp

eval            : ID
                | exp 'cond_op' eval
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