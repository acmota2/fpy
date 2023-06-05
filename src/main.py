import argparse
import os
import sys
import grammar_written
import re
import syntaxer


parser = argparse.ArgumentParser(
                    prog='Functional FPY transpiler to python',
                    description='Transpiles fpy code to runnable python 3.9+ code.',
                    epilog='Made with ply and yacc')
parser.add_argument('filename')
parser.add_argument('-o', '--output-file-name', dest="outFileName")

def write_to_file(code, file):
    text_file = open(file, "w")
    text_file.write(code)
    text_file.close()

def read_file(filePath):
    text_file = open(filePath, "r")
    code = text_file.read()
    text_file.close()
    return code

def process_std_lib(destination_folder):
    s = grammar_written.gen_code(read_file("./code_construction/fpystdlib.py"))
    s = re.sub(r"std\.", "", s)
    write_to_file(s, destination_folder + "__fpylib.py")

if __name__ == '__main__':
    args = parser.parse_args()
    code = ""
    outFolder = "./"
    output = "./out.py"
    code = read_file(args.filename) if args.filename else sys.stdin.read()
    if (args.outFileName):
        output = args.outFileName
        outFolder = os.path.dirname(output) + "/"
    if syntaxer.parse_types(code):
        code = "import __fpylib as std\n" + grammar_written.gen_code(code)
        write_to_file(code, output)
        process_std_lib(outFolder)
