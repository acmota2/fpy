#!/bin/zsh

case $1 in
    'yacc_test')
        python ./testing/python_files/grammar_tester.py
        ;;
    'lex_test')
        python ./testing/python_files/lexer_tester.py
        ;;
    'lex_check')
        python lexer.py
        ;;
    'type_test')
        python syntaxer.py
        ;;
    '')
        python main.py
        ;;
    *)
        echo Bad argument!
        ;;
esac
