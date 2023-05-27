import sys

l = [x.rstrip() for x in sys.stdin.readlines()]
bla = l[0].split(',')

print(
f'''
def p_{bla[0]}(p): "{bla[0]} : {l[2]}" ; p[0] = p[1]

def p_{bla[0]}_infix(p):
    "{bla[0]} : {l[1]}"
    p[0] = ti.infix_checker(p[1], {bla[1]}, p[3])
    if not p[0]:
        parser.err_type = err.err_types.type
        print(err.fpy_type_error(make_error_text(p), p[2].return_, p[3], p.lexer.lineno))
        raise SyntaxError

def p_{bla[0]}_right_infix(p):
    "{bla[0]} : {l[3]}"
    p[0] = ti.right_infix_checker(p[2], {bla[1]})
    if not p[0]:
        parser.err_type = err.err_types.type
        print(err.fpy_type_error(make_error_text(p), p[3].return_, p[2], p.lexer.lineno))
        raise SyntaxError

def p_{bla[0]}_left_infix(p):
    "{bla[0]} : {l[4]}"
    p[0] = ti.left_infix_checker(p[3], {bla[1]})
    if not p[0]:
        parser.err_type = err.err_types.type
        err.fpy_type_error(make_error_text(p), p[2].return_, p[3], p.lexer.lineno)
        raise SyntaxError
''')
