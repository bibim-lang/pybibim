from rply import LexerGenerator

op_map = {
    'NUMBER': r'\d[\d\s]*',
    'PLUS': r'\+',
    'MINUS': r'-',
    'MUL': r'\*',
    'DIV': r'/',
    'EXPR_OPEN': r'\(',
    'EXPR_CLOSE': r'\)',
    'AND': r'&',
    'OR': r'\|',
    'NOT': r'!',
    'EQ': r'\?\s*=',
    'GT': r'>',
    'LT': r'<',
    'PACK': r':',
    'PACK_OPEN': r'{',
    'PACK_CLOSE': r'}',
    'LINE_OPEN': r'\[',
    'LINE_SEP': r';',
    'LINE_CLOSE': r'\]',
    'ASS': r'=',
    'DENO': r'\^',
    'MEM': r'@',
}

lg = LexerGenerator()
for name, regex in op_map.items():
    lg.add(name, regex)

lg.ignore('\s+')
lg.ignore('~#((?!#~).)*#~')

lexer = lg.build()
