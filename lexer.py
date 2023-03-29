from ply import lex
import sys

reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'fdef': 'FDEF',
    'lambda': 'LAMBDA',
    'or': 'OR',
    'and': 'AND'
}

tokens = [
    # limits
    'BEGIN','END',
    # vars
    'ID','NUM','ASSIGN','REASSIGN','COMMA','STRING','CHAR',
    # open/close
    'LPAR','RPAR','LBRACKET','RBRACKET','LBRACE','RBRACE',
    # cond
    'COND','COLON',
    # list [head|tail]
    'LISTER',
    # aritm
    'SUM','PROD','DIV','SUB','MOD','POW','INTDIV',
    # conditional
    'EQ','LT','GT','LTE','GTE','DIF',
] + list(reserved.values())

states = (
   ('fpy','exclusive'),
)

t_ignore = r'.*'

t_fpy_ignore = f'\r\n '

t_fpy_ignore_COMMENT = r'\#.*'

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

def t_fpy_ASSIGN(t):
    r':='
    return t

t_fpy_REASSIGN = r'='

def t_fpy_COMMA(t):
    r','
    return t

def t_fpy_LPAR(t):
    r'\('
    return t

def t_fpy_RPAR(t):
    r'\)'
    return t

def t_fpy_LBRACKET(t):
    r'\['
    return t

def t_fpy_RBRACKET(t):
    r'\]'
    return t

def t_fpy_LBRACE(t):
    r'\{'
    return t

def t_fpy_RBRACE(t):
    r'\}'
    return t

t_fpy_COND = r'\[\?\.\.\?\]'

def t_fpy_COLON(t):
    r':'
    return t

def t_fpy_LISTER(t):
    r'\|'
    return t

def t_fpy_SUM(t):
    r'\+'
    return t

def t_fpy_SUB(t):
    r'-'
    return t

def t_fpy_PROD(t):
    r'\*'
    return t

def t_fpy_DIV(t):
    r'\/'
    return t

def t_fpy_INTDIV(t):
    r'\/\/'
    return t

def t_fpy_POW(t):
    r'\*\*'
    return t

def t_fpy_EQ(t):
    r'=='
    return t

def t_fpy_LT(t):
    r'<'
    return t

def t_fpy_GT(t):
    r'>'
    return t

t_fpy_LTE = r'<='
t_fpy_GTE = r'>='
t_fpy_DIF = r'!='

def t_error(t):
    t.lexer.skip(1)

def t_fpy_error(t):
    print(f'Error on line {t.lexer.lineno}, position {t.lexer.lexpos}')
    t.lexer.skip(1)

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
