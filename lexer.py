import ply.lex as lex
import sys
import re

arrow_matcher = re.compile(r'\-\>')

reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'fdef': 'FDEF',
    'let': 'LET',
    'int':'INT',
    'float':'FLOAT',
    'char':'CHAR',
    'bool':'BOOL',
    'alias':'ALIAS',
}

tokens = [
    # limits
    'BEGIN','END',
    # types
    'TYPECLASS','INTT','FLOATT','STRINGT','CHART','BOOLT',
    # vars
    'ID','SPECIALID',
    # cond
    'COND',
    # range
    'RANGER',
    # arrows
    'RARROW',
] + list(reserved.values())

literals = ['[',']','(',')','{','}',',','=','|',':','`']

states = (
   ('fpy','exclusive'),
)

t_ignore = ' \t\n'

t_fpy_ignore = '\t\r\n '

def t_fpy_ignore_COMMENT(t):
    r'\#.*'
    pass

def t_fpy_SPECIALID(t):
    r"(([\!@$%\^&\*\-\/\\.;<>|\+]\=*)|(\=([\!@#$%\^&\*\-\/\\.;<>|\+\=])+))+"
    t.type = 'RARROW' if arrow_matcher.match(t.value) else 'SPECIALID'
    return t

t_fpy_TYPECLASS = r"[A-Z]\w*"

def t_fpy_RARROW(t):
    r'->'
    return t

def t_fpy_RANGER(t):
    r'\.\.'
    return t

def t_fpy_EQUAL(t):
    r'='
    t.type = '='
    return t

def t_fpy_LISTER(t):
    r'\|'
    t.type = '|'
    return t

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

def t_fpy_newline(t):
    r'\n'
    t.lexer.lineno += 1

def t_BEGIN(t):
    r'(.|\n)*(\'{3}fpy|\"{3}fpy)'
    t.lexer.begin('fpy')
    return t

def t_fpy_END(t):
     r'((\'{3})|(\"{3}))(.|\n)*'
     t.lexer.begin('INITIAL')
     return t

def t_fpy_ID(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value,'ID')
    return t

t_fpy_INTT = r'\d+'

def t_fpy_FLOATT(t):
    r'\d+.\d+((e|E)\d+)?'
    return t

def t_fpy_STRINGT(t):
    r'\"[^\"]*\"'
    return t

def t_fpy_CHART(t):
    r'\'[^\']\''
    return t

def t_fpy_BOOLT(t):
    r'True|False'
    return t

t_fpy_COND = r'\[\?\.\.\?\]'


def t_error(t):
    t.lexer.skip(1)

def t_fpy_error(t):
    print(f'Error on line {t.lexer.lineno}, position {t.lexer.lexpos}')
    t.lexer.skip(1)

lexer = lex.lex()

# for testing purposes
if __name__ == '__main__':
    data = sys.stdin.read() if len(sys.argv) == 1 else open(sys.argv).read()
    lexer = lex.lex()
    lexer.input(data)
    toks = []
    for tok in lexer:
        toks.append(tok)
    print(f'''
Tamanho da lista: {len(toks)}
Lista:
{toks}''')
