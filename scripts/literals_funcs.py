func = ['+', '-', '*', '/', '%', '^', '<', '>']

literals = ['[',']','(',')','{','}',',','=','|',':','`'] + func

i = 1
for l in literals:
    print(f"def t_l{i}(t): r'\{l}' ; pass")
    i += 1