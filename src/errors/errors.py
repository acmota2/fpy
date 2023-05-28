from enum import Enum

red_bold = lambda x: f'\x1b[1;31m{x}\x1b[0;0m'
yellow_bold = lambda x: f'\x1b[1;33m{x}\x1b[0;0m'
cyan_bold = lambda x: f'\x1b[1;36m{x}\x1b[0;0m'
bold = lambda x: f"\x1b[1;1m{x}\x1b[0;0m"

err_types = Enum('err_types', ['redef', 'call', 'type', 'name', 'scope'])

warning = lambda x: f'''
{yellow_bold("Warning:")}
    {x}'''

def variable_not_in_scope(name, line):
    print(f"""
{red_bold("Error:")} variable {bold(name)}, first appearing on line {line}, not in scope""")

def empty_call(line):
    print(f"""{warning(f"Empty function call on line {line} is redundant")}""")

def argument_warning(self, fname, line_info):
    print(warning(f"Case of {cyan_bold(fname)} on line {line_info} is unreacheable"))

def non_callable(obj, type_, line_info):
    print(f"\n{red_bold('Error')}: Element {cyan_bold(obj)}, on line {line_info}, of type {cyan_bold(type_)}, doesn't accept arguments")

def fpy_type_error(obj, expected_type, actual_type, line):
    print(f'''
{red_bold("Error:")} expected type for {bold(obj)} on line {line} could not be inferred
    {bold(obj)} actual type is {yellow_bold(actual_type)}
    {bold(obj)} expected type is {red_bold(expected_type)}''')

def name_already_defined(name, cur_line, prev_line):
    print(f'''
{red_bold("Fatal:")} name {bold(name)} defined on line {cur_line} already in use by global value on line {prev_line}''')

def function_redefinition(name, cur_line, prev_line):
    print(f'''
{red_bold("Fatal:")} name {bold(name)} defined on line {cur_line} already in use by function on line {prev_line}''')

def reserved_function_redefinition(name, cur_line):
    print(f'''
{red_bold("Fatal:")} name {cyan_bold(name)} defined on line {cur_line} is reserved and can't be redefined''')

def impossible_function_case(name, line):
    print(warning(f"""Using function name for pattern matching with {cyan_bold(name)} at {line}
Pattern match is redundant"""))

def alias_inexistant(name, line):
    print(f"{red_bold('Error:')} no valid equivalence for that type could be found")
