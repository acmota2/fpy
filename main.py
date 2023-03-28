'''
GRAMMAR

S           : begin 'fpy' code end
code        : code fun
func        : 'fdef' id '(' args ')' '{' body '}'
args        : pattern
            | args ',' pattern
pattern     : id
            | num
            | '(' args ')'
            | '[' list_p_cont
list_p_cont : ']'
            | list_pattern ']'
list_pattern: pattern
            | pattern '|' list_pattern
body        : statement
            | body statement
statement   : id ':=' exp
            | id '=' exp
            | pattern '=' exp
            | exp
exp         : var
            | pattern
            | eval
            | aritm
            | cond
            | '(' exp ')'
cond        : '?..?' '{' condition '}'
            | 'if' eval 'then' exp 'else' exp
condition   : eval ':' exp '\n' '_' ':' exp
            | eval ':' exp '\n' condition '\n' '_' ':' exp
eval        : id
            | eval 'cond_op' exp
aritm       : num
            | id
            | aritm 'artim_op' exp
var         : id
            | num
            | list
            | tuple
list        : '['
list_cont   : ']'
            | list_term ']'
list_term   : exp
            | list_term ',' exp
tuple       : '('
            | tuple_cont ')'
tuple_cont  : exp
            | tuple_cont ',' exp
'''

import ply.yacc as yacc

if __name__ == '__main__':
    ...