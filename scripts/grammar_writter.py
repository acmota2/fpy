import re
import sys

f = open('grammar.txt', 'r')
output = open('grammar_written.py', 'w')

print('''from lexer import tokens, literals
import ply.yacc as yacc
''', file=output)

grammar = f.readlines()
cur_prod = ''
matcher = re.compile(r'([a-z]\w*)?\s*(:|\|)\s*(.*)')
prod = 0
for x in grammar:
    if x == '\n': 
        continue
    m = matcher.match(x)
    if m and m.group(2) == ':':
        prod = 0
        cur_prod = m.group(1)
    print(f'''def p_{cur_prod}{prod if prod else ''}(p):
    "{cur_prod} : {m.group(3)}"
'''
    , file=output)
    prod += 1

print('parser = yacc.yacc()', file=output)
