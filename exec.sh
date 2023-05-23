#!/bin/zsh

case $1 in
    'grammar_test')
        python tester.py
        ;;
    'lex_test')
        python lexer.py
        ;;
    'type_test')
        python syntaxer.py
        ;;
    *)
        python main.py
        ;;
esac
