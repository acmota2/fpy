import ply.lex as lex
import sys

reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'fdef': 'FDEF',
    'let': 'LET',
}

tokens = [
    # limits
    'BEGIN','END',
    # vars
    'ID','SPECIALID','NUM','STRING','CHAR','BOOL',
    # cond
    'COND',
    # range
    'RANGER',
] + list(reserved.values())

literals = ['[',']','(',')','{','}',',','=','|',':','`']

states = (
   ('fpy','exclusive'),
)

t_ignore = ' \t\n'

t_fpy_ignore = '\t\r\n '

t_fpy_ignore_COMMENT = r'\#.*'

t_fpy_SPECIALID = r"([\!@#$%\^&\*\-\/\\.;<>|\+]\=*)|(\=\=+)+"

def t_fpy_RANGER(t):
    r'\.\.'
    return t

def t_fpy_EQUAL(t):
    r'=[^=]'
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
    r'(\'{3}fpy|\"{3}fpy)'
    t.lexer.begin('fpy')
    return t

def t_fpy_END(t):
     r'((\'{3})|(\"{3}))'
     t.lexer.begin('INITIAL')
     return t

def t_fpy_ID(t):
    r'[a-zA-Z_]\w*'
    t.type = reserved.get(t.value,'ID')
    return t


def t_fpy_NUM(t):
    r'(-\+)?\d+(.\d+)?'
    return t

def t_fpy_STRING(t):
    r'\"[^\"]*\"'
    return t

def t_fpy_CHAR(t):
    r'\'[^\']\''
    return t

def t_fpy_BOOL(t):
    r'True|False'
    return t

def t_fpy_ASSIGN(t):
    r':='
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
