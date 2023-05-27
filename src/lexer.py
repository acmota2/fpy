import ply.lex as lex
import sys

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
    'undefined':'UNDEFINED',
    # misc
    '//': 'DIV',
    '->':'RARROW',
    # conditionals
    '||': 'OR',
    '&&': 'AND',
    '==':'EQ',
    '!=':'NEQ',
    '>=':'GTE',
    '<=':'LTE',
}

tokens = [
    # limits
    'BEGIN','END',
    # types
    'INTT','FLOATT','STRINGT','CHART','BOOLT',
    # vars
    'ID','SPECIALID',
    # cond
    'COND',
    # range
    'RANGER',
] + list(reserved.values())

func = ['+', '-', '*', '/', '%', '^', '<', '>']

literals = ['[',']','(',')','{','}',',','=','|',':','`'] + func

def get_literal(check: str, default: str):
    for t in literals:
        if check == t:
            return t
    return default

states = (
   ('fpy','exclusive'),
)

t_ignore = '\t\r '

t_fpy_ignore = '\t\r '

def t_python(t): r'(.+)\'\'\'fpy' ; pass
def t_l1(t): r'\[' ; pass
def t_l2(t): r'\]' ; pass
def t_l3(t): r'\(' ; pass
def t_l4(t): r'\)' ; pass
def t_l5(t): r'\{' ; pass
def t_l6(t): r'\}' ; pass
def t_l7(t): r'\,' ; pass
def t_l8(t): r'\=' ; pass
def t_l9(t): r'\|' ; pass
def t_l10(t): r'\:' ; pass
def t_l11(t): r'\`' ; pass
def t_l12(t): r'\+' ; pass
def t_l13(t): r'\-' ; pass
def t_l14(t): r'\*' ; pass
def t_l15(t): r'\/' ; pass
def t_l16(t): r'\%' ; pass
def t_l17(t): r'\^' ; pass
def t_l18(t): r'\<' ; pass
def t_l19(t): r'\>' ; pass

def t_fpy_ignore_COMMENT(t):
    r'\#.*'
    pass

def t_fpy_RARROW(t): r'\->' ; t.type = 'RARROW' ; return t

def t_fpy_SPECIALID(t):
    r"(-(?!(\d))|[\~\+\\\/\=@\^&\*$%\!\.><;][\~\+\\\/\=@\^&\*$%\!\.><;\-]*)"
    initial_type = t.type
    t.type = reserved.get(t.value, 'SPECIALID')
    if initial_type == t.type:
        t.type = get_literal(t.value, 'SPECIALID')
    return t

def t_fpy_RANGER(t):
    r'\.\.'
    return t

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1
    t.lexer.dif = t.lexer.lexpos

def t_fpy_newline(t):
    r'\n'
    t.lexer.lineno += 1
    t.lexer.dif = t.lexer.lexpos

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

t_fpy_INTT = r'(-|\+)?\d+'

def t_fpy_FLOATT(t): r'(-|\+)?\d+\.\d+((e|E)(\+|-)?\d+)?' ; return t
def t_fpy_STRINGT(t): r'\"[^\"]*\"' ; return t
def t_fpy_CHART(t): r'\'[^\']\'' ; return t
def t_fpy_BOOLT(t): r'True|False' ; return t

t_fpy_COND = r'\[\?\.\.\?\]'

def t_error(t):
    t.lexer.skip(1)

def t_fpy_error(t):
    print(f'Error on line {t.lexer.lineno}, position {t.lexer.lexpos - t.lexer.dif + 1}')
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
