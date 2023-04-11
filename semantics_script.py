from os import listdir
import re

def get_classes(f):
    cur_file = open(f'./semantics/{f}', 'r').read()
    class_finder = re.compile(r'(?<=class\s)[_a-zA-Z]\w*')
    return ', '.join(class_finder.findall(cur_file))


files = [f for f in listdir('./semantics') if f != '__init__.py']

init = open('./semantics/__init__.py', 'w')

for name in files:
    print(
        f"from .{name.split('.py')[0]} import {get_classes(name)}",
        file=init)
