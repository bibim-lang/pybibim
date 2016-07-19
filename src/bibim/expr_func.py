# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from . import datatype
from .utils import safe_get_value, safe_get_evaled_expr


class Func:
    """ Expr이 평가될 때 실행된 함수를 정의하는 class입니다.

    세부적인 동작은 해당 class를 상속받은 class에서 정의합니다.
    """

    def __call__(self):
        """ Expr이 평가될 때 실행되는 method입니다.

        :return: 평가된 결과
        :rtype: datatype.ValueExpr
        """
        return datatype.NULL_EXPR_INST


class FuncBowl(Func):
    """ bowl operator ':'의 동작을 정의하는 class입니다. """

    def __init__(self, bowl=None, nn=None):
        """ FuncBowl를 생성합니다.

        :param bowl: Expr를 가져올 Bowl instance
        :type bowl: Bowl
        :param nn: bowl의 noodle number
        :type nn: Number
        """
        self.bowl = bowl
        self.nn = nn

    def __call__(self):
        """ Expr이 평가될 때 실행되는 method입니다.

        :return: 평가된 결과
        :rtype: datatype.ValueExpr
        """
        bowl = safe_get_value(self.bowl, datatype.Bowl)
        if bowl is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        nn = safe_get_value(self.nn, datatype.Number)
        if nn is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        try:
            return safe_get_evaled_expr(bowl.get_noodle(nn).expr)
        except KeyError:
            return datatype.NULL_EXPR_INST


class FuncAssign(Func):
    """ assign operator '='의 동작을 정의하는 class입니다. """

    def __init__(self, bowl=None, nn=None, value_expr=None):
        """ FuncAssign를 생성합니다.

        만약 bowl이 None이라면 기본값으로 datatype.ValueExpr(datatype.MEM)를
        사용합니다.

        :param bowl: assign 대상
        :type bowl: Bowl
        :param nn: bowl의 noodle number
        :type nn: Number
        :param value_expr: assign할 Value를 가진 ValueExpr
        :type value_expr: ValueExpr
        """
        self.bowl = bowl if bowl is not None else datatype.ValueExpr(
            datatype.MEM)
        self.nn = nn
        self.value_expr = value_expr

    def __call__(self):
        """ Expr이 평가될 때 실행되는 method입니다.

        :return: 평가된 결과
        :rtype: datatype.ValueExpr
        """
        bowl = safe_get_value(self.bowl, datatype.Bowl)
        if bowl is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        nn = safe_get_value(self.nn, datatype.Number)
        if nn is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        value_expr = safe_get_evaled_expr(self.value_expr)
        bowl.set_noodle(nn, value_expr)
        return datatype.NULL_EXPR_INST


class FuncDeno(Func):
    """ denominator operator '^'의 동작을 정의하는 class입니다. """

    def __init__(self, number=None):
        """ FuncDeno를 생성합니다.

        :param number: 분모를 가져올 대상
        :type number: Number
        """
        self.number = number

    def __call__(self):
        """ Expr이 평가될 때 실행되는 method입니다.

        :return: 평가된 결과
        :rtype: datatype.ValueExpr
        """
        number = safe_get_value(self.number, datatype.Number)
        if number is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        return datatype.ValueExpr(number.denominator_number())


class FuncPlus(Func):
    """ add operator '+'의 동작을 정의하는 class입니다. """

    def __init__(self, l_number=None, r_number=None):
        """ FuncPlus를 생성합니다.

        :param l_number: operator의 좌측 number
        :type l_number: Number
        :param r_number: operator의 우측 number
        :type r_number: Number
        """
        self.l_number = l_number
        self.r_number = r_number

    def __call__(self):
        """ Expr이 평가될 때 실행되는 method입니다.

        :return: 평가된 결과
        :rtype: datatype.ValueExpr
        """
        l_number = safe_get_value(self.l_number, datatype.Number)
        if l_number is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        r_number = safe_get_value(self.r_number, datatype.Number)
        if r_number is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        return datatype.ValueExpr(l_number + r_number)


class FuncMinus(Func):
    """ subtract operator '-'의 동작을 정의하는 class입니다. """

    def __init__(self, l_number=None, r_number=None):
        """ FuncMinus를 생성합니다.

        :param l_number: operator의 좌측 number
        :type l_number: Number
        :param r_number: operator의 우측 number
        :type r_number: Number
        """
        self.l_number = l_number
        self.r_number = r_number

    def __call__(self):
        """ Expr이 평가될 때 실행되는 method입니다.

        :return: 평가된 결과
        :rtype: datatype.ValueExpr
        """
        l_number = safe_get_value(self.l_number, datatype.Number)
        if l_number is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        r_number = safe_get_value(self.r_number, datatype.Number)
        if r_number is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        return datatype.ValueExpr(l_number - r_number)


class FuncMul(Func):
    """ multiply operator '*'의 동작을 정의하는 class입니다. """

    def __init__(self, l_number=None, r_number=None):
        """ FuncMul를 생성합니다.

        :param l_number: operator의 좌측 number
        :type l_number: Number
        :param r_number: operator의 우측 number
        :type r_number: Number
        """
        self.l_number = l_number
        self.r_number = r_number

    def __call__(self):
        """ Expr이 평가될 때 실행되는 method입니다.

        :return: 평가된 결과
        :rtype: datatype.ValueExpr
        """
        l_number = safe_get_value(self.l_number, datatype.Number)
        if l_number is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        r_number = safe_get_value(self.r_number, datatype.Number)
        if r_number is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        return datatype.ValueExpr(l_number * r_number)


class FuncNumberSep(Func):
    """ number separator '/'의 동작을 정의하는 class입니다. """

    def __init__(self, l_number=None, r_number=None):
        """ FuncNumberSep 생성합니다.

        :param l_number: operator의 좌측 number
        :type l_number: Number
        :param r_number: operator의 우측 number
        :type r_number: Number
        """
        self.l_number = l_number
        self.r_number = r_number

    def __call__(self):
        """ Expr이 평가될 때 실행되는 method입니다.

        :return: 평가된 결과
        :rtype: datatype.ValueExpr
        """
        l_number = safe_get_value(self.l_number, datatype.Number)
        if l_number is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        r_number = safe_get_value(self.r_number, datatype.Number)
        if r_number is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        return datatype.ValueExpr(l_number / r_number)


class FuncAnd(Func):
    """ and operator '&'의 동작을 정의하는 class입니다. """

    def __init__(self, l_number=None, r_number=None):
        """ FuncAnd를 생성합니다.

        :param l_number: operator의 좌측 number
        :type l_number: Number
        :param r_number: operator의 우측 number
        :type r_number: Number
        """
        self.l_number = l_number
        self.r_number = r_number

    def __call__(self):
        """ Expr이 평가될 때 실행되는 method입니다.

        :return: 평가된 결과
        :rtype: datatype.ValueExpr
        """
        l_number = safe_get_value(self.l_number, datatype.Number)
        if l_number is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        r_number = safe_get_value(self.r_number, datatype.Number)
        if r_number is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        return datatype.ValueExpr(l_number and r_number)


class FuncOr(Func):
    """ or operator '|'의 동작을 정의하는 class입니다. """

    def __init__(self, l_number=None, r_number=None):
        """ FuncOr를 생성합니다.

        :param l_number: operator의 좌측 number
        :type l_number: Number
        :param r_number: operator의 우측 number
        :type r_number: Number
        """
        self.l_number = l_number
        self.r_number = r_number

    def __call__(self):
        """ Expr이 평가될 때 실행되는 method입니다.

        :return: 평가된 결과
        :rtype: datatype.ValueExpr
        """
        l_number = safe_get_value(self.l_number, datatype.Number)
        if l_number is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        r_number = safe_get_value(self.r_number, datatype.Number)
        if r_number is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        return datatype.ValueExpr(l_number or r_number)


class FuncNot(Func):
    """ not operator '!'의 동작을 정의하는 class입니다. """

    def __init__(self, number=None):
        """ FuncNot을 생성합니다.

        :param number: not을 취할 number
        :type number: Number
        """
        self.number = number

    def __call__(self):
        """ Expr이 평가될 때 실행되는 method입니다.

        :return: 평가된 결과
        :rtype: datatype.ValueExpr
        """
        number = safe_get_value(self.number, datatype.Number)
        if number is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        return datatype.ValueExpr(number.not_f())


class FuncEq(Func):
    """ equal operator '?='의 동작을 정의하는 class입니다. """

    def __init__(self, l_number=None, r_number=None):
        """ FuncEq를 생성합니다.

        :param l_number: operator의 좌측 number
        :type l_number: Number
        :param r_number: operator의 우측 number
        :type r_number: Number
        """
        self.l_number = l_number
        self.r_number = r_number

    def __call__(self):
        """ Expr이 평가될 때 실행되는 method입니다.

        :return: 평가된 결과
        :rtype: datatype.ValueExpr
        """
        l_number = safe_get_value(self.l_number, datatype.Number)
        if l_number is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        r_number = safe_get_value(self.r_number, datatype.Number)
        if r_number is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        return datatype.ValueExpr(l_number.eq_f(r_number))


class FuncGt(Func):
    """ greater than operator '>'의 동작을 정의하는 class입니다. """

    def __init__(self, l_number=None, r_number=None):
        """ FuncGt를 생성합니다.

        :param l_number: operator의 좌측 number
        :type l_number: Number
        :param r_number: operator의 우측 number
        :type r_number: Number
        """
        self.l_number = l_number
        self.r_number = r_number

    def __call__(self):
        """ Expr이 평가될 때 실행되는 method입니다.

        :return: 평가된 결과
        :rtype: datatype.ValueExpr
        """
        l_number = safe_get_value(self.l_number, datatype.Number)
        if l_number is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        r_number = safe_get_value(self.r_number, datatype.Number)
        if r_number is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        return datatype.ValueExpr(l_number.gt_f(r_number))


class FuncLt(Func):
    """ less than operator '<'의 동작을 정의하는 class입니다. """

    def __init__(self, l_number=None, r_number=None):
        """ FuncLt를 생성합니다.

        :param l_number: operator의 좌측 number
        :type l_number: Number
        :param r_number: operator의 우측 number
        :type r_number: Number
        """
        self.l_number = l_number
        self.r_number = r_number

    def __call__(self):
        """ Expr이 평가될 때 실행되는 method입니다.

        :return: 평가된 결과
        :rtype: datatype.ValueExpr
        """
        l_number = safe_get_value(self.l_number, datatype.Number)
        if l_number is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        r_number = safe_get_value(self.r_number, datatype.Number)
        if r_number is datatype.NULL_INST:
            return datatype.NULL_EXPR_INST
        return datatype.ValueExpr(l_number.lt_f(r_number))
