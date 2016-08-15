# -*- coding: utf-8 -*-
from __future__ import absolute_import

from rply import ParserGenerator

from . import datatype, io
from .expr_func import *
from .lexer import op_map
from .utils import filtered_str

pg = ParserGenerator(
    list(op_map.keys()),
    precedence=[
        ('left', ['ASSIGN']),
        ('left', ['ass_expr']),
        ('left', ['AND', 'OR']),
        ('left', ['NOT']),
        ('left', ['EQ', 'GT', 'LT']),
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL']),
        ('left', ['BOWL']),
        ('left', ['DENO']),
        ('left', ['NUMBER_SEP']),
        ('left', ['NOODLE_SEP']),
        ('left', ['BOWL_OPEN', 'BOWL_CLOSE']),
        ('left', ['NOODLE_OPEN', 'NOODLE_CLOSE']),
        ('left', ['EXPR_OPEN', 'EXPR_CLOSE']),
        ('left', ['MEM']),
        ('left', ['NUMBER']),
    ]
)


@pg.production('bowl : BOWL_OPEN BOWL_CLOSE')
def bowl_empty(_):
    return datatype.Bowl(None)


@pg.production('bowl : BOWL_OPEN wad BOWL_CLOSE')
def bowl_wad(p):
    wad = p[1]
    return datatype.Bowl(wad)


@pg.production('number : NUMBER')
def number(p):
    number_str = filtered_str(p[0].getstr())
    number_int = int(number_str)
    return datatype.Number(number_int)


@pg.production('noodle : NOODLE_OPEN expr NOODLE_SEP expr NOODLE_CLOSE')
def noodle(p):
    nn = p[1]
    expr = p[3]
    return datatype.Noodle(nn, expr)


@pg.production('wad : noodle')
def wad_single(p):
    _noodle = p[0]
    return datatype.Wad(_noodle)


@pg.production('wad : wad noodle')
def wad_put(p):
    wad = p[0]
    _noodle = p[1]
    return wad.put(_noodle)


@pg.production('expr : number')
@pg.production('expr : bowl')
def expr_single(p):
    value = p[0]
    return datatype.ValueExpr(value)


@pg.production('expr : EXPR_OPEN expr EXPR_CLOSE')
def expr_parans(p):
    expr = p[1]
    return expr


@pg.production('expr : expr BOWL expr ASSIGN expr', precedence='ass_expr')
def expr_assign(p):
    bowl = p[0]
    nn = p[2]
    value_expr = p[4]
    return datatype.Expr(FuncAssign(bowl=bowl, nn=nn, value_expr=value_expr))


@pg.production('expr : MEM BOWL expr ASSIGN expr', precedence='ass_expr')
def expr_assign_m(p):
    bowl = datatype.ValueExpr(datatype.MEM)
    nn = p[2]
    value_expr = p[4]
    return datatype.Expr(FuncAssign(bowl=bowl, nn=nn, value_expr=value_expr))


@pg.production('expr : expr BOWL expr')
def expr_bowl_get(p):
    bowl = p[0]
    nn = p[2]
    return datatype.Expr(FuncBowl(bowl=bowl, nn=nn))


@pg.production('expr : MEM BOWL expr')
def expr_bowl_get_m(p):
    bowl = datatype.ValueExpr(datatype.MEM)
    nn = p[2]
    return datatype.Expr(FuncBowl(bowl=bowl, nn=nn))


@pg.production('expr : DENO expr')
def expr_deno(p):
    _number = p[1]
    return datatype.Expr(FuncDeno(number=_number))


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


@pg.production('expr : expr NUMBER_SEP expr')
def expr_num_sep(p):
    l_number = p[0]
    r_number = p[2]
    return datatype.Expr(FuncNumberSep(l_number=l_number, r_number=r_number))


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
    _number = p[1]
    return datatype.Expr(FuncNot(number=_number))


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
    if token.source_pos:
        raise gen_error("Ran into a '%s' where it was't expected at %s:%s" % (
            token.value, token.source_pos.lineno, token.source_pos.colno))
    else:
        raise gen_error("Unexpected error on parsing token '%s'" % (token.value,))


def gen_error(msg):
    io.write_data(io.STDOUT, ("Parse Error: %s\n" % (msg,)).decode("utf-8"))
    return ValueError(msg)



parser = pg.build()
