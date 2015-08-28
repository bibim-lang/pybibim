# coding=utf-8
from rply import ParserGenerator, Token
from expr_func import *
from lexer import op_map
import datatype
from utils import filtered_str

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
def bowl_empty(p):
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
    noodle = p[0]
    return datatype.Wad(noodle)


@pg.production('wad : wad noodle')
def wad_put(p):
    wad = p[0]
    noodle = p[1]
    return wad.put(noodle)


@pg.production('expr : number')
@pg.production('expr : bowl')
def expr_single(p):
    value = p[0]
    return datatype.ValueExpr(value)


@pg.production('expr : EXPR_OPEN expr EXPR_CLOSE')
def expr_parans(p):
    expr = p[1]
    return expr


@pg.production('expr : MEM BOWL expr ASSIGN expr', precedence='ass_expr')
@pg.production('expr : expr BOWL expr ASSIGN expr', precedence='ass_expr')
def expr_assign_m(p):
    if type(p[0]) is Token and p[0].gettokentype() == 'MEM':
        bowl = datatype.ValueExpr(datatype.MEM)
    else:
        bowl = p[0]
    nn = p[2]
    value_expr = p[4]
    return datatype.Expr(FuncAssign(bowl=bowl, nn=nn, value_expr=value_expr))


@pg.production('expr : expr BOWL expr')
@pg.production('expr : MEM BOWL expr')
def expr_bowl_get(p):
    if type(p[0]) is Token and p[0].gettokentype() == 'MEM':
        bowl = datatype.ValueExpr(datatype.MEM)
    else:
        bowl = p[0]
    nn = p[2]
    return datatype.Expr(FuncBowl(bowl=bowl, nn=nn))


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
