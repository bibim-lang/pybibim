from rply import ParserGenerator, Token
from expr_func import *
from lexer import op_map
import datatype
from utils import filtered_str

pg = ParserGenerator(
    list(op_map.keys()),
    precedence=[
        ('left', ['ASS']),
        ('left', ['NUMBER']),
        ('left', ['ass_expr', 'ass_expr_m']),
        ('left', ['MEM']),
        ('left', ['PACK_OPEN', 'PACK_CLOSE']),
        ('left', ['LINE_OPEN', 'LINE_CLOSE']),
        ('left', ['EXPR_OPEN', 'EXPR_CLOSE']),
        ('left', ['LINE_SEP']),
        ('left', ['AND', 'OR']),
        ('left', ['NOT']),
        ('left', ['EQ', 'GT', 'LT']),
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL']),
        ('left', ['PACK']),
        ('left', ['DENO']),
        ('left', ['DIV']),
    ]
)


@pg.production('pack : PACK_OPEN PACK_CLOSE')
def pack_empty(p):
    return datatype.Pack(None)


@pg.production('pack : PACK_OPEN lines PACK_CLOSE')
def pack_lines(p):
    lines = p[1]
    return datatype.Pack(lines)


@pg.production('number : NUMBER')
def number(p):
    number_str = filtered_str(p[0].getstr())
    number_int = int(number_str)
    return datatype.Number(number_int)


@pg.production('line : LINE_OPEN expr LINE_SEP expr LINE_CLOSE')
def line(p):
    ln = p[1]
    expr = p[3]
    return datatype.Line(ln, expr)


@pg.production('lines : line')
def lines_single(p):
    line = p[0]
    return datatype.LineList(line)


@pg.production('lines : lines line')
def lines_combine(p):
    lines = p[0]
    line = p[1]
    return lines.append(line)


@pg.production('expr : number')
@pg.production('expr : pack')
def expr_single(p):
    value = p[0]
    return datatype.ValueExpr(value)


@pg.production('expr : EXPR_OPEN expr EXPR_CLOSE')
def expr_parans(p):
    expr = p[1]
    return expr


@pg.production('expr : MEM PACK expr ASS expr', precedence='ass_expr_m')
@pg.production('expr : expr PACK expr ASS expr', precedence='ass_expr')
def expr_assign_m(p):
    if type(p[0]) is Token and p[0].gettokentype() == 'MEM':
        pack = datatype.ValueExpr(datatype.MEM)
    else:
        pack = p[0]
    ln = p[2]
    value_expr = p[4]
    return datatype.Expr(FuncAssign(pack=pack, ln=ln, value_expr=value_expr))


@pg.production('expr : expr PACK expr')
@pg.production('expr : MEM PACK expr')
def expr_pack_get(p):
    if type(p[0]) is Token and p[0].gettokentype() == 'MEM':
        pack = datatype.ValueExpr(datatype.MEM)
    else:
        pack = p[0]
    ln = p[2]
    return datatype.Expr(FuncPack(pack=pack, ln=ln))


@pg.production('expr : DENO expr')
def expr_deno(p):
    number = p[1]
    return datatype.Expr(FuncDeno(number=number))


@pg.production('expr : expr PLUS expr')
def expr_plus(p):
    l_number = p[0]
    r_number = p[2]
    return datatype.Expr(FuncPlus(l_number=l_number, r_number=r_number))


@pg.production('expr : expr MINUS expr')
def expr_minus(p):
    l_number = p[0]
    r_number = p[2]
    return datatype.Expr(FuncMinus(l_number=l_number, r_number=r_number))


@pg.production('expr : expr MUL expr')
def expr_multiply(p):
    l_number = p[0]
    r_number = p[2]
    return datatype.Expr(FuncMul(l_number=l_number, r_number=r_number))


@pg.production('expr : expr DIV expr')
def expr_divide(p):
    l_number = p[0]
    r_number = p[2]
    return datatype.Expr(FuncDiv(l_number=l_number, r_number=r_number))


@pg.production('expr : expr AND expr')
def expr_and(p):
    l_number = p[0]
    r_number = p[2]
    return datatype.Expr(FuncAnd(l_number=l_number, r_number=r_number))


@pg.production('expr : expr OR expr')
def expr_or(p):
    l_number = p[0]
    r_number = p[2]
    return datatype.Expr(FuncOr(l_number=l_number, r_number=r_number))


@pg.production('expr : NOT expr')
def expr_not(p):
    number = p[1]
    return datatype.Expr(FuncNot(number=number))


@pg.production('expr : expr EQ expr')
def expr_eq(p):
    l_number = p[0]
    r_number = p[2]
    return datatype.Expr(FuncEq(l_number=l_number, r_number=r_number))


@pg.production('expr : expr GT expr')
def expr_gt(p):
    l_number = p[0]
    r_number = p[2]
    return datatype.Expr(FuncGt(l_number=l_number, r_number=r_number))


@pg.production('expr : expr LT expr')
def expr_lt(p):
    l_number = p[0]
    r_number = p[2]
    return datatype.Expr(FuncLt(l_number=l_number, r_number=r_number))


@pg.error
def error_handler(token):
    raise ValueError("Ran into a '%s' where it was't expected at %s:%s" % (
        token.value, token.source_pos.lineno, token.source_pos.colno))


parser = pg.build()
