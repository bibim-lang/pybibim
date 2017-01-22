# -*- coding: utf-8 -*-
from __future__ import absolute_import
from rply.token import BaseBox
from rpython.rlib.rbigint import rbigint
from rpython.rlib import jit

from . import io


class Base(BaseBox):
    """ Base class는 아무 역할도 하지 않습니다.

    대신, 모든 Datatype의 부모 class로 동작하여 다형성을 유지합니다.
    """
    _immutable_ = True

    def log_string(self):
        return "Base"

    def log_expr(self):
        return "B"


class Value(Base):
    """ Value class는 아무 역할도 하지 않습니다.

    대신, Null, Number, Bowl의 부모 class로 동작하여 다형성을 유지합니다.
    """
    _immutable_ = True

    def log_string(self):
        return "Value"

    def log_expr(self):
        return "V"


class Expr(Base):
    """ Expr class는 Bibim의 Expression 입니다. """
    _immutable_ = True
    _immutable_fields_ = ["_func"]

    def __init__(self, func):
        """ ExprFunc Func instance로 새 expr를 만듭니다.

        :param func: Expr이 평가될 때 실행될 Func
        :type func: Func
        """
        self._func = func

    def eval(self):
        """ Expr을 평가한 결과를 반환합니다.

        :return: 평가 결과
        :rtype: ValueExpr
        """
        return self._func.call()

    def log_string(self):
        return "Expr(%s)" % (self._func.log_string(),)

    def log_expr(self):
        return "%s" % (self._func.log_expr(),)


class ValueExpr(Expr):
    _immutable_ = True
    _immutable_fields_ = ["_value"]

    def __init__(self, value):
        """ Value를 가지는 새로운 ValueExpr을 만듭니다.

        :param value: ValueExpr이 평가될 때 반환할 Value
        :type value: Value
        """
        self._value = value

    @jit.elidable
    def eval(self):
        """ ValueExpr을 평가한 결과를 반환합니다.

        :return: 평가 결과
        :rtype: ValueExpr
        """
        return self

    @jit.elidable
    def value(self):
        """ 해당 ValueExpr의 value를 반환합니다.

        :return: value
        :rtype: Value
        """
        return self._value

    def log_string(self):
        return "ValueExpr(%s)" % (self._value.log_string())

    def log_expr(self):
        return "%s" % (self._value.log_expr(),)


class Null(Value):
    """ 정의되지 않은 값을 가지는 Value입니다."""
    _immutable_ = True

    def log_string(self):
        return "Null"

    def log_expr(self):
        return "Null"


class Number(Value):
    """ 기약분수 꼴로 표현되는 유리수를 가지는 Value입니다. """
    _immutable_ = True
    _immutable_fields_ = ["_numerator", "_denominator"]

    R_ZERO = rbigint.fromint(0)
    R_ONE = rbigint.fromint(1)

    @staticmethod
    def ONE():
        if not hasattr(Number, "ONE_V"):
            Number.ONE_V = Number(Number.R_ONE)
        return Number.ONE_V

    @staticmethod
    def ZERO():
        if not hasattr(Number, "ZERO_V"):
            Number.ZERO_V = Number(Number.R_ZERO)
        return Number.ZERO_V

    @staticmethod
    @jit.elidable
    def gcd(a, b):
        """ 정수 a와 b의 최소공배수를 계산합니다.
        :type a: rbigint
        :type b: rbigint
        """
        while b.ne(Number.R_ZERO):
            a, b = b, a.mod(b)
        return a

    def __init__(self, numerator, denominator=None):
        """ 새로운 Number를 하나 이상의 정수로부터 만듭니다.

        분모를 정의하지 않았을 경우, 기본적으로 1이 사용됩니다.

        :param numerator: 분자
        :type numerator: rbigint
        :param denominator: 분모
        :type denominator: rbigint
        """

        if denominator is None:
            denominator = Number.R_ONE

        if denominator.eq(Number.R_ZERO):
            raise AssertionError('Zero cannot be a denominator.')

        if denominator.eq(Number.R_ONE):
            self._numerator = numerator
            self._denominator = Number.R_ONE
        else:
            g = Number.gcd(numerator, denominator)
            self._numerator = numerator.div(g)
            self._denominator = denominator.div(g)

    @jit.elidable
    def numerator(self):
        """ Number의 분자를 정수로 반환합니다.

        :return: 분자
        :rtype: rbigint
        """
        return self._numerator

    @jit.elidable
    def denominator(self):
        """ Number의 분모를 정수로 반환합니다.

        :return: 분모
        :rtype: rbigint
        """
        return self._denominator

    @jit.elidable
    def denominator_number(self):
        """ Number의 분모를 반환합니다.

        denominator property의 경우 rbigint를 반환하지만, 이 method는 Number 객체를
        반환합니다.

        :return: 분모
        :rtype: Number
        """
        return Number(self._denominator)

    @jit.elidable
    def __nonzero__(self):
        """ Number 값이 Number.ZERO일 경우 False를, 그 외의 경우에는 True를 반환합니다.

        만약 Bibim code의 논리 연산 및 비교 연산 결과가 필요할 때에는 이 method의 실행 결과를
        직접 반환하면 안됩니다. 각 논리 및 비교 연산의 결과는 Number.ONE() 또는 Number.ZERO을
        반환하도록 해야 합니다. 해당 결과를 원한다면, bool_f 메서드를 대신 사용하세요.
        """
        return self._numerator.ne(Number.R_ZERO)

    @staticmethod
    @jit.elidable
    def from_bool(bool_value):
        """ bool_value가 True면 Number.ONE을, 그 외의 경우에는 Number.ZERO을 반환합니다.

        :param bool_value: 변환할 bool값
        :type bool_value: bool
        :return: 변환 결과
        :rtype: Number
        """
        return Number.ONE() if bool_value is True else Number.ZERO()

    @jit.elidable
    def bool_f(self):
        """ Number 값이 Number.ZERO일 경우 Number.ZERO를, 그 외의 경우에는 Number.ONE을
        반환합니다.

        :return: 연산 결과
        :rtype: Number
        """
        return Number.ZERO() if self._numerator.eq(Number.R_ZERO) else Number.ONE()

    @jit.elidable
    def neg(self):
        """ -number 값을 반환합니다.

        :return: 연산 결과
        :rtype: Number
        """
        return Number(self.numerator().neg(), self.denominator())

    @jit.elidable
    def mul(self, other):
        """ number와 other의 곱을 반환합니다.

        :param other: 곱할 Number
        :type other: Number
        :return: 곱
        :rtype: Number
        """
        if not isinstance(other, Number):
            # if mode == MODE_DEBUG:
            #     raise AssertionError('Numbers only can be calculated with '
            #                          'a Number but %s is not a Number.' % (
            #                              other.log_string(),))
            # else:
            #     return NULL_INST
            return NULL_INST
        return Number(self.numerator().mul(other.numerator()),
                      self.denominator().mul(other.denominator()))

    @jit.elidable
    def add(self, other):
        """ number와 other의 합을 반환합니다.

        :param other: 더할 Number
        :type other: Number
        :return: 합
        :rtype: Number
        """
        if not isinstance(other, Number):
            # if mode == MODE_DEBUG:
            #     raise AssertionError('Numbers only can be calculated with '
            #                          'a Number but %s is not a Number.' % (
            #                              other.log_string(),))
            # else:
            #     return NULL_INST
            return NULL_INST
        return Number(
            self._numerator.mul(other.denominator()).add(
                self.denominator().mul(other.numerator())
            ),
            self.denominator().mul(other.denominator()))

    @jit.elidable
    def sub(self, other):
        """ number와 other의 차를 반환합니다.

        :param other: 뺄 Number
        :type other: Number
        :return: 차
        :rtype: Number
        """
        if not isinstance(other, Number):
            # if mode == MODE_DEBUG:
            #     raise AssertionError('Numbers only can be calculated with '
            #                          'a Number but %s is not a Number.' % (
            #                              other.log_string(),))
            # else:
            #     return NULL_INST
            return NULL_INST
        return self.add(other.neg())

    @jit.elidable
    def div(self, other):
        """ 자신을 분자로 하고 other를 분모로 하는 새로운 Number를 생성합니다.

        :param other: 분모로 사용할 Number
        :type other: Number
        :return: 새 Number
        :rtype: Number
        """
        if not isinstance(other, Number):
            # if mode == MODE_DEBUG:
            #     raise AssertionError('Numbers only can be calculated with '
            #                          'a Number but %s is not a Number.' % (
            #                              other.log_string(),))
            # else:
            #     return NULL_INST
            return NULL_INST
        return Number(self.numerator().mul(other.denominator()),
                      self.denominator().mul(other.numerator()))

    @jit.elidable
    def _and(self, other):
        """ 자신과 other가 모두 Number.ZERO이 아닌 경우는 Number.ONE을, 그 외의
        경우에는 Number.ZERO을 반환합니다.

        :param other: 연산할 Number
        :type other: Number
        :return: 연산 결과
        :rtype: Number
        """
        if isinstance(other, Number):
            if self.numerator().ne(Number.R_ZERO) and other.numerator().ne(Number.R_ZERO):
                return Number.ONE()
            else:
                return Number.ZERO()
        elif isinstance(other, Value):
            return Number.ZERO()
        else:
            # if mode == MODE_DEBUG:
            #     raise AssertionError('Numbers only can be calculated logically'
            #                          ' with a Value but %s is not a Value.' % (
            #                              other.log_string(),))
            # else:
            #     return Number.ZERO()
            return Number.ZERO()

    @jit.elidable
    def _or(self, other):
        """ 자신과 other가 모두 Number.ZERO인 경우는 Number.ZERO을, 그 외의
        경우에는 Number.ONE을 반환합니다.

        :param other: 연산할 Number
        :type other: Number
        :return: 연산 결과
        :rtype: Number
        """
        if self.numerator().ne(Number.R_ZERO):
            return Number.ONE()
        else:
            if isinstance(other, Number):
                return other.bool_f()
            elif isinstance(other, Value):
                return Number.ZERO()
            else:
                # if mode == MODE_DEBUG:
                #     raise AssertionError('Numbers only can be calculated '
                #                          'logically with a Value but %s is '
                #                          'not a Value.' % (other.log_string(),))
                # else:
                #     return Number.ZERO()
                return Number.ZERO()

    @jit.elidable
    def lt(self, other):
        """ 자신이 other보다 작을 경우 True를, 그 외의 경우에는 False을
        반환합니다.

        :param other: 연산할 Number
        :type other: Number
        """
        if not isinstance(other, Number):
            # if mode == MODE_DEBUG:
            #     raise AssertionError('Numbers only can be compared with '
            #                          'a Number but %s is not a Number.' % (
            #                              other.log_string(),))
            # else:
            #     return False
            return False
        return self.numerator().mul(other.denominator()).lt(
            other.numerator().mul(self.denominator())
        )

    @jit.elidable
    def gt(self, other):
        """ 자신이 other보다 클 경우 True를, 그 외의 경우에는 False을
        반환합니다.

        :param other: 연산할 Number
        :type other: Number
        """
        if not isinstance(other, Number):
            # if mode == MODE_DEBUG:
            #     raise AssertionError('Numbers only can be compared with '
            #                          'a Number but %s is not a Number.' % (
            #                              other.log_string(),))
            # else:
            #     return False
            return False
        return self.numerator().mul(other.denominator()).gt(
           other.numerator().mul(self.denominator())
        )

    @jit.elidable
    def eq(self, other):
        """ 자신이 other보다 작을 경우 True를, 그 외의 경우에는 False을
        반환합니다.

        :param other: 연산할 Number
        :type other: Number
        """
        if not isinstance(other, Number):
            # if mode == MODE_DEBUG:
            #     raise AssertionError('Numbers only can be compared with '
            #                          'a Number but %s is not a Number.' % (
            #                              other.log_string(),))
            # else:
            #     return False
            return False
        return self.numerator().eq(other.numerator()) and \
               self.denominator().eq(other.denominator())

    @jit.elidable
    def not_f(self):
        """ 자신이 Number.ZERO이면 Number.ONE을, 그 외의 경우에는 Number.ZERO을
        반환합니다.

        :return: 연산 결과
        :rtype: Number
        """
        return Number.ONE() if self._numerator.eq(Number.R_ZERO) else Number.ZERO()

    @jit.elidable
    def eq_f(self, other):
        """ other와 자신이 같으면 Number.ONE을, 다르면 Number.ZERO을 반환합니다.

        :param other: 비교할 Number
        :type other: Number
        :return: 비교 결과
        :rtype: Number
        """
        return Number.from_bool(self.eq(other))

    @jit.elidable
    def gt_f(self, other):
        """ 자신이 other보다 크면 Number.ONE을, 작거나 같으면 Number.ZERO을
        반환합니다.

        :param other: 비교할 Number
        :type other: Number
        :return: 비교 결과
        :rtype: Number
        """
        return Number.from_bool(self.gt(other))

    @jit.elidable
    def lt_f(self, other):
        """ 자신이 other보다 작으면 Number.ONE을, 크거나 같으면 Number.ZERO을
        반환합니다.

        :param other: 비교할 Number
        :type other: Number
        :return: 비교 결과
        :rtype: Number
        """
        return Number.from_bool(self.lt(other))

    def log_string(self):
        if self._denominator.eq(Number.R_ONE):
            return "%s" % (self._numerator.str(),)
        else:
            return "%s/%s" % (self._numerator.str(), self._denominator.str())

    def log_expr(self):
        if self._denominator.eq(Number.R_ONE):
            return "%s" % (self._numerator.str(),)
        else:
            return "%s/%s" % (self._numerator.str(), self._denominator.str())


class Noodle(Base):
    """ Wad에 담길 Noodle class입니다. """
    _immutable_ = None

    def __init__(self, nn_expr, expr):
        """ 새로운 Noodle을 생성합니다.

        :param nn_expr: Noodle의 Noodle number
        :type nn_expr: Expr
        :param expr: Noodle의 Expr
        :type expr: Expr
        """
        self._nn_expr = nn_expr
        self._expr = expr

    @jit.elidable
    def nn_expr(self):
        """ Noodle의 noodle number를 반환합니다.

        :return: noodle number
        :rtype: Expr
        """
        return self._nn_expr

    def expr(self):
        """ Noodle의 Expr을 반환합니다.

        :return: Expr
        :rtype: Expr
        """
        return self._expr

    def set_expr(self, expr):
        """ Noodle의 Expr을 등록합니다.

        :return: NullExpr
        :rtype: NullExpr
        """
        self._expr = expr
        return NULL_EXPR_INST

    def log_string(self):
        return "[%s; %s]" % (self.nn_expr().log_string(), self._expr.log_string())

    def log_expr(self):
        return "[%s; %s]" % (self.nn_expr().log_expr(), self._expr.log_expr())


class Wad(Base):
    """ Bowl의 Noodle들을 담고 있는 class입니다. """
    _immutable_ = None

    def __init__(self, noodle):
        """ 새로운 Wad를 생성합니다.

        :param noodle: noodle
        :type noodle: Noodle|None
        """

        if noodle:
            self._noodles = [noodle]
        else:
            self._noodles = []

    def noodles(self):
        """ noodles를 반환합니다.

        :return: Noodles
        :rtype: list[Noodle]
        """
        return self._noodles

    def put(self, noodle):
        """ noodles에 noodle을 추가합니다.

        :param noodle: 추가할 noodle
        :return: Wad
        """
        self._noodles.append(noodle)
        return self

    def log_string(self):
        result = ""
        for noodle in self._noodles:
            result += noodle.log_string()
        return result

    def log_expr(self):
        result = ""
        for noodle in self._noodles:
            result += noodle.log_expr()
        return result


class Bowl(Value):
    """ Wad를 담는 Bowl class입니다. """
    _immutable_ = None

    def __init__(self, wad):
        """ wad로부터 새로운 Bowl을 생성합니다.

        :param wad: 담을 wad
        :type wad: Wad|None
        """
        if wad:
            self._wad = wad
        else:
            self._wad = Wad(None)

    def wad(self):
        """ wad를 반환합니다.

        :return: wad
        :rtype: Wad
        """
        return self._wad

    @staticmethod
    @jit.elidable
    def from_str(s):
        """ 문자열을 Bowl으로 변환합니다.

        :param s: 변환할 문자열
        :type s: unicode
        :return: 생성된 Bowl
        :rtype: Bowl
        """
        wad = Wad(None)
        noodle_num = Number.ZERO()
        for c in s.decode("utf-8"):
            wad.put(Noodle(ValueExpr(noodle_num), ValueExpr(Number(rbigint.fromint(ord(c))))))
            noodle_num = noodle_num.add(Number.ONE())
        return Bowl(wad)

    @staticmethod
    def to_str(bowl):
        """ Bowl을 문자열로 변환합니다.

        :param bowl: 변환할 Bowl
        :type bowl: Bowl
        :return: 생성된 문자열
        :rtype: unicode
        """
        result = u''
        index = 0
        while True:
            try:
                noodle = bowl.get_noodle(Number(rbigint.fromint(index)))
            except KeyError:
                break
            noodle_value = noodle.expr().eval().value()
            if not isinstance(noodle_value, Number):
                raise gen_error("Could not convert it to string, "
                                "noodle value is not a Number: %s" % (
                                    noodle_value.log_string()))
            elif noodle_value.denominator().ne(Number.R_ONE):
                raise gen_error("Could not convert it to string, "
                                "noodle value's denominator is not 1: %s"
                                % (noodle_value.log_string()))
            result += unichr(noodle_value.numerator().toint())
            index += 1
        return result

    def get_noodle(self, number):
        """ number를 noodle number로 가지는 Noodle을 반환합니다.

        :param number: 가져올 Noodle의 noodle number
        :type number: Number
        :return: 해당 Noodle
        :rtype: Noodle
        """
        for noodle in self.wad().noodles():
            nn = noodle.nn_expr().eval().value()
            if not isinstance(nn, Number):
                raise gen_error("Noodle numbers must be a Number. %s is "
                                "not a Number" % (nn.log_string(),))
            if nn.eq(number):
                return noodle
        raise KeyError("Cannot found the noodle")

    def set_noodle(self, number, value_expr):
        """ number를 noodle number로 가지는 Noodle의 expr를 변경합니다.

        :param number: 수정할 Noodle의 noodle number
        :type number: Number
        :param value_expr: 수정할 Noodle의 expr
        :type value_expr: ValueExpr
        :return: NullExpr
        :rtype: NullExpr
        """
        for noodle in self.wad().noodles():
            nn = noodle.nn_expr().eval().value()
            if not isinstance(nn, Number):
                raise gen_error("Noodle numbers must be a Number. %s is "
                                "not a Number" % (nn.log_string(),))
            if nn.eq(number):
                noodle.set_expr(value_expr)
                return NULL_EXPR_INST
        self.wad().put(Noodle(ValueExpr(number), value_expr))
        return NULL_EXPR_INST

    def log_string(self):
        return "{%s}" % (self._wad.log_string(),)

    def log_expr(self):
        return "{%s}" % (self._wad.log_expr(),)


class Memory(Bowl):
    """ '@' 문자에 매핑되는 특수 Bowl class입니다. """
    _immutable_ = None

    NN_CURRENT_NOODLE = Number.ZERO()
    NN_IO = Number.ONE()

    def __init__(self):
        """ 새로운 Memory을 생성합니다. """
        Bowl.__init__(self, None)

    def get_noodle(self, number):
        """ number를 noodle number로 가지는 Noodle을 반환합니다.

        만약 number가 NN_IO일 경우, 표준 입력에서 문자열을 가져와 Noodle의 expr에
        Bowl으로 변환해 담아서 반환합니다. 모든 입력은 utf-8로 인코딩합니다.

        :param number: 가져올 Noodle의 noodle number
        :type number: Number
        :return: 해당 Noodle
        :rtype: Noodle
        """
        if number.eq(Memory.NN_IO):
            input_str = io.read_data(io.STDIN)
            return Noodle(ValueExpr(Memory.NN_IO),
                          ValueExpr(Bowl.from_str(input_str)))
        else:
            return Bowl.get_noodle(self, number)

    def set_noodle(self, number, value_expr):
        """ number를 noodle number로 가지는 Noodle의 expr를 변경합니다.

        만약 number가 NN_IO일 경우, 표준 출력으로 value_expr의 내용을
        문자열로 변환해 출력합니다.

        또, number가 NN_CURRENT_NOODLE 경우 바로 NullExpr을 반환합니다.
        만약 현재 noodle number의 값을 update해야 할 경우
        set_current_noodle_number method를 대신 사용하세요.

        :param number: 수정할 Noodle의 noodle number
        :type number: Number
        :param value_expr: 수정할 Noodle의 expr
        :type value_expr: ValueExpr
        :return: NullExpr
        :rtype: NullExpr
        """
        if number.eq(Memory.NN_IO):
            bowl_to_print = value_expr.value()
            if not isinstance(bowl_to_print, Bowl):
                raise gen_error("Could not print it as string, "
                                "expr is not a Bowl: %s" % (
                                    bowl_to_print.log_string()))
            io.write_data(io.STDOUT, Bowl.to_str(bowl_to_print))
            return NULL_EXPR_INST
        elif number.eq(Memory.NN_CURRENT_NOODLE):
            return NULL_EXPR_INST
        else:
            return Bowl.set_noodle(self, number, value_expr)

    def set_current_noodle_number(self, value_expr):
        """ 현재 noodle number를 지정합니다.
        :param value_expr: 현재 Noodle number의 ValueExpr
        :type value_expr: ValueExpr
        :return: NullExpr
        :rtype: NullExpr
        """
        return Bowl.set_noodle(self, Memory.NN_CURRENT_NOODLE, value_expr)

    def log_string(self):
        result = "{"
        for noodle in self.wad().noodles():
            result += noodle.log_string()
        return result + "}"

    def log_expr(self):
        return "@"

    def log_contents(self):
        result = "{"
        for noodle in self.wad().noodles():
            result += "\n  " + noodle.log_expr()
        return result + "\n}"


def gen_error(msg):
    io.write_data(io.STDOUT, ("Runtime Error: %s\n" % (msg,)).decode("utf-8"))
    return RuntimeError(msg)


NULL_INST = Null()
NULL_EXPR_INST = ValueExpr(NULL_INST)
MEM = Memory()