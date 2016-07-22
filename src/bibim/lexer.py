# -*- coding: utf-8 -*-
from __future__ import absolute_import

from rply import LexerGenerator

op_map = {
    'NUMBER': r'\d[\d\s]*',
    'PLUS': r'\+',
    'MINUS': r'-',
    'MUL': r'\*',
    'NUMBER_SEP': r'/',
    'EXPR_OPEN': r'\(',
    'EXPR_CLOSE': r'\)',
    'AND': r'&',
    'OR': r'\|',
    'NOT': r'!',
    'EQ': r'\?\s*=',
    'GT': r'>',
    'LT': r'<',
    'BOWL': r':',
    'BOWL_OPEN': r'{',
    'BOWL_CLOSE': r'}',
    'NOODLE_OPEN': r'\[',
    'NOODLE_SEP': r';',
    'NOODLE_CLOSE': r'\]',
    'ASSIGN': r'=',
    'DENO': r'\^',
    'MEM': r'@',
}

lg = LexerGenerator()
for name, regex in op_map.items():
    lg.add(name, regex)

lg.ignore('\s+')
lg.ignore('~\s*#((?!#~).)*#\s*~')

lexer = lg.build()
