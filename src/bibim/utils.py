# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .mode import mode, MODE_DEBUG
from . import datatype


def filtered_str(string):
    result = ''
    for c in string:
        if not c.isspace():
            result += c
    return result


# def safe_get_evaled_expr(expr):
#     if mode == MODE_DEBUG:
#         assert isinstance(expr, datatype.Expr), \
#             "expr is must be an Expr but expr is not an Expr: %s" \
#             % (repr(expr),)
#         evaled_expr = expr.eval()
#         assert isinstance(evaled_expr, datatype.ValueExpr), \
#             "evaled_expr is must be an ValueExpr but evaled_expr is not an " \
#             "ValueExpr: %s" % (repr(evaled_expr),)
#         return evaled_expr
#     else:
#         try:
#             return expr.eval()
#         except:
#             return datatype.NULL_EXPR_INST

def safe_get_evaled_expr(expr):
    try:
        return expr.eval()
    except:
        return datatype.NULL_EXPR_INST


# def safe_get_value(expr, cls=None, is_null_ok=True):
#     if mode == MODE_DEBUG:
#         value = safe_get_evaled_expr(expr).value()
#         is_null = value is datatype.NULL_INST
#         if is_null and not is_null_ok:
#             raise AssertionError(
#                 "value is must be not an Null but value is an Null: %s")
#         elif not isinstance(value, datatype.Value):
#             raise AssertionError(
#                 "value is must be an Value but value is not an Value: %s"
#                 % (repr(value),))
#         if not is_null and cls is not None:
#             assert isinstance(value, cls), \
#                 "value is must be an %s but value is not an %s: %s" \
#                 % (cls.__name__, cls.__name__, repr(value),)
#         return value
#     else:
#         try:
#             return expr.eval().value()
#         except:
#             return datatype.NULL_INST


def safe_get_value(expr, cls=None, is_null_ok=True):
    try:
        return expr.eval().value()
    except:
        return datatype.NULL_INST
