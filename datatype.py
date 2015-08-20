import io
import sys
import pybibim


class Value:
    """ Value class는 아무 역할도 하지 않습니다.

    대신, Null, Number, Pack의 부모 class로 동작하여 다형성을 유지합니다.
    """
    pass


class Expr:
    """ Expr class는 Bibim의 Expression 입니다. """
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
        return self._func()

    def __repr__(self):
        return "Expr(%s)" % (repr(self._func),)


class ValueExpr(Expr):
    def __init__(self, value):
        """ Value를 가지는 새로운 ValueExpr을 만듭니다.

        :param value: ValueExpr이 평가될 때 반환할 Value
        :type value: Value
        """
        self._value = value

    def eval(self):
        """ ValueExpr을 평가한 결과를 반환합니다.

        :return: 평가 결과
        :rtype: ValueExpr
        """
        return self

    @property
    def value(self):
        """ 해당 ValueExpr의 value를 반환합니다.

        :return: value
        :rtype: Value
        """
        return self._value

    def __repr__(self):
        return "ValueExpr(%s)" % (repr(self._value))


class Null(Value):
    """ 정의되지 않은 값을 가지는 Value입니다."""

    def __repr__(self):
        return "Null"


class Number(Value):
    """ 기약분수 꼴로 표현되는 유리수를 가지는 Value입니다. """
    @staticmethod
    def gcd(a, b):
        """ 정수 a와 b의 최소공배수를 계산합니다. """
        while b:
            a, b = b, a % b
        return a

    def __init__(self, numerator, denominator=1):
        """ 새로운 Number를 하나 이상의 정수로부터 만듭니다.

        분모를 정의하지 않았을 경우, 기본적으로 1이 사용됩니다.

        :param numerator: 분자
        :type numerator: int
        :param denominator: 분모
        :type denominator: int
        """

        if denominator == 0:
            raise AssertionError('Zero cannot be a denominator.')

        if denominator == 1:
            self._numerator = numerator
            self._denominator = 1
        else:
            g = Number.gcd(numerator, denominator)
            self._numerator = numerator // g
            self._denominator = denominator // g

    @property
    def numerator(self):
        """ Number의 분자를 정수로 반환합니다.

        :return: 분자
        :rtype: int
        """
        return self._numerator

    @property
    def denominator(self):
        """ Number의 분모를 정수로 반환합니다.

        :return: 분모
        :rtype: int
        """
        return self._denominator

    def denominator_number(self):
        """ Number의 분모를 반환합니다.

        denominator property의 경우 int를 반환하지만, 이 method는 Number 객체를
        반환합니다.

        :return: 분모
        :rtype: Number
        """
        return Number(self._denominator)

    def __bool__(self):
        """ Number 값이 Number(0)일 경우 False를, 그 외의 경우에는 True를 반환합니다.

        만약 Bibim code의 논리 연산 및 비교 연산 결과가 필요할 때에는 이 method의 실행 결과를
        직접 반환하면 안됩니다. 각 논리 및 비교 연산의 결과는 Number(1) 또는 Number(0)을
        반환하도록 해야 합니다. 해당 결과를 원한다면, bool_f 메서드를 대신 사용하세요.
        """
        return self._numerator != 0

    @staticmethod
    def from_bool(bool_value):
        """ bool_value가 True면 Number(1)을, 그 외의 경우에는 Number(0)을 반환합니다.

        :param bool_value: 변환할 bool값
        :type bool_value: bool
        :return: 변환 결과
        :rtype: Number
        """
        return Number(1) if bool_value is True else Number(0)

    def bool_f(self):
        """ Number 값이 Number(0)일 경우 Number(0)를, 그 외의 경우에는 Number(1)을
        반환합니다.

        :return: 연산 결과
        :rtype: Number
        """
        return Number.from_bool(bool(self))

    def __neg__(self):
        """ -number 값을 반환합니다.

        :return: 연산 결과
        :rtype: Number
        """
        return Number(-self.numerator, self.denominator)

    def __mul__(self, other):
        """ number와 other의 곱을 반환합니다.

        :param other: 곱할 Number
        :type other: Number
        :return: 곱
        :rtype: Number
        """
        if not isinstance(other, Number):
            if pybibim.mode == pybibim.MODE_DEBUG:
                raise AssertionError('Numbers only can be calculated with '
                                     'a Number but %s is not a Number.' % (
                                         repr(other),))
            else:
                return NULL_INST
        return Number(self.numerator * other.numerator,
                      self.denominator * other.denominator)

    def __add__(self, other):
        """ number와 other의 합을 반환합니다.

        :param other: 더할 Number
        :type other: Number
        :return: 합
        :rtype: Number
        """
        if not isinstance(other, Number):
            if pybibim.mode == pybibim.MODE_DEBUG:
                raise AssertionError('Numbers only can be calculated with '
                                     'a Number but %s is not a Number.' % (
                                         repr(other),))
            else:
                return NULL_INST
        return Number(
            self._numerator * other.denominator
            + self.denominator * other.numerator,
            self.denominator * other.denominator)

    def __sub__(self, other):
        """ number와 other의 차를 반환합니다.

        :param other: 뺄 Number
        :type other: Number
        :return: 차
        :rtype: Number
        """
        if not isinstance(other, Number):
            if pybibim.mode == pybibim.MODE_DEBUG:
                raise AssertionError('Numbers only can be calculated with '
                                     'a Number but %s is not a Number.' % (
                                         repr(other),))
            else:
                return NULL_INST
        return self + (-other)

    def __truediv__(self, other):
        """ 자신을 분자로 하고 other를 분모로 하는 새로운 Number를 생성합니다.

        :param other: 분모로 사용할 Number
        :type other: Number
        :return: 새 Number
        :rtype: Number
        """
        if not isinstance(other, Number):
            if pybibim.mode == pybibim.MODE_DEBUG:
                raise AssertionError('Numbers only can be calculated with '
                                     'a Number but %s is not a Number.' % (
                                         repr(other),))
            else:
                return NULL_INST
        return Number(self.numerator * other.denominator,
                      self.denominator * other.numerator)

    def __and__(self, other):
        """ 자신과 other가 모두 Number(0)이 아닌 경우는 Number(1)을, 그 외의
        경우에는 Number(0)을 반환합니다.

        :param other: 연산할 Number
        :type other: Number
        :return: 연산 결과
        :rtype: Number
        """
        if isinstance(other, Number):
            if self.numerator != 0 and other.numerator != 0:
                return Number(1)
            else:
                return Number(0)
        elif isinstance(other, Value):
            return Number(0)
        else:
            if pybibim.mode == pybibim.MODE_DEBUG:
                raise AssertionError('Numbers only can be calculated logically'
                                     ' with a Value but %s is not a Value.' % (
                                         repr(other),))
            else:
                return Number(0)

    def __or__(self, other):
        """ 자신과 other가 모두 Number(0)인 경우는 Number(0)을, 그 외의
        경우에는 Number(1)을 반환합니다.

        :param other: 연산할 Number
        :type other: Number
        :return: 연산 결과
        :rtype: Number
        """
        if self.numerator != 0:
            return Number(1)
        else:
            if isinstance(other, Number):
                return other.bool_f()
            elif isinstance(other, Value):
                return Number(0)
            else:
                if pybibim.mode == pybibim.MODE_DEBUG:
                    raise AssertionError('Numbers only can be calculated '
                                         'logically with a Value but %s is '
                                         'not a Value.' % (repr(other),))
                else:
                    return Number(0)

    def __lt__(self, other):
        """ 자신이 other보다 작을 경우 True를, 그 외의 경우에는 False을
        반환합니다.

        :param other: 연산할 Number
        :type other: Number
        """
        if not isinstance(other, Number):
            if pybibim.mode == pybibim.MODE_DEBUG:
                raise AssertionError('Numbers only can be compared with '
                                     'a Number but %s is not a Number.' % (
                                         repr(other),))
            else:
                return False
        return self.numerator * other.denominator < \
               other.numerator * self.denominator

    def __gt__(self, other):
        """ 자신이 other보다 클 경우 True를, 그 외의 경우에는 False을
        반환합니다.

        :param other: 연산할 Number
        :type other: Number
        """
        if not isinstance(other, Number):
            if pybibim.mode == pybibim.MODE_DEBUG:
                raise AssertionError('Numbers only can be compared with '
                                     'a Number but %s is not a Number.' % (
                                         repr(other),))
            else:
                return False
        return self.numerator * other.denominator > \
               other.numerator * self.denominator

    def __eq__(self, other):
        """ 자신이 other보다 작을 경우 True를, 그 외의 경우에는 False을
        반환합니다.

        :param other: 연산할 Number
        :type other: Number
        """
        if not isinstance(other, Number):
            if pybibim.mode == pybibim.MODE_DEBUG:
                raise AssertionError('Numbers only can be compared with '
                                     'a Number but %s is not a Number.' % (
                                         repr(other),))
            else:
                return False
        return self.numerator == other.numerator and \
               self.denominator == other.denominator

    def not_f(self):
        """ 자신이 Number(0)이면 Number(1)을, 그 외의 경우에는 Number(0)을
        반환합니다.

        :return: 연산 결과
        :rtype: Number
        """
        return Number.from_bool(not bool(self))

    def eq_f(self, other):
        """ other와 자신이 같으면 Number(1)을, 다르면 Number(0)을 반환합니다.

        :param other: 비교할 Number
        :type other: Number
        :return: 비교 결과
        :rtype: Number
        """
        return Number.from_bool(self == other)

    def gt_f(self, other):
        """ 자신이 other보다 크면 Number(1)을, 작거나 같으면 Number(0)을
        반환합니다.

        :param other: 비교할 Number
        :type other: Number
        :return: 비교 결과
        :rtype: Number
        """
        return Number.from_bool(self > other)

    def lt_f(self, other):
        """ 자신이 other보다 작으면 Number(1)을, 크거나 같으면 Number(0)을
        반환합니다.

        :param other: 비교할 Number
        :type other: Number
        :return: 비교 결과
        :rtype: Number
        """
        return Number.from_bool(self < other)

    def __repr__(self):
        if self._denominator == 1:
            return "%d" % (self._numerator,)
        else:
            return "%d/%d" % (self._numerator, self._denominator)


class Line:
    """ LineList에 담길 Line class입니다. """
    def __init__(self, ln_expr, expr):
        """ 새로운 Line을 생성합니다.

        :param ln_expr: Line의 line number
        :type ln_expr: Expr
        :param expr: Line의 Expr
        :type expr: Expr
        """
        self._ln_expr = ln_expr
        self._expr = expr

    @property
    def ln_expr(self):
        """ Line의 line number를 반환합니다.

        :return: line number
        :rtype: Expr
        """
        return self._ln_expr

    @property
    def expr(self):
        """ Line의 Expr을 반환합니다.

        :return: Expr
        :rtype: Expr
        """
        return self._expr

    def set_expr(self, expr):
        """ Line의 Expr을 등록합니다.

        :return: NullExpr
        :rtype: NullExpr
        """
        self._expr = expr
        return NULL_EXPR_INST

    def __repr__(self):
        return "[%s; %s]" % (repr(self.ln_expr), repr(self._expr))


class LineList:
    """ Pack의 Line들을 담고 있는 class입니다. """
    def __init__(self, line):
        """ 새로운 LineList 생성합니다.

        :param line: Line
        :type line: Line|None
        """

        if line:
            self._lines = [line]
        else:
            self._lines = list()

    @property
    def lines(self):
        """ lines를 반환합니다.

        :return: Lines
        :rtype: list[Line]
        """
        return self._lines

    def append(self, line):
        """ lines에 line을 추가합니다.

        :param line: 추가할 line
        :return: LineList
        """
        self._lines.append(line)
        return self

    def __repr__(self):
        return "".join(repr(line) for line in self._lines)


class Pack(Value):
    """ LineList를 담는 Pack class입니다. """
    def __init__(self, line_list):
        """ line_list로부터 새로운 Pack을 생성합니다.

        :param line_list: line_list
        :type line_list: LineList|None
        """
        if line_list:
            self._line_list = line_list
        else:
            self._line_list = LineList(None)

    @property
    def line_list(self):
        """ line_list를 반환합니다.

        :return: line_list
        :rtype: LineList
        """
        return self._line_list

    @staticmethod
    def from_str(s):
        """ 문자열을 Pack으로 변환합니다.

        :param s: 변환할 문자열
        :type s: str
        :return: 생성된 Pack
        :rtype: Pack
        """
        line_list = LineList(None)
        ln = Number(0)
        for c in s:
            line_list.append(Line(ValueExpr(ln), ValueExpr(Number(ord(c)))))
            ln = ln + Number(1)
        return Pack(line_list)

    @staticmethod
    def to_str(pack):
        """ Pack을 문자열로 변환합니다.

        :param pack: 변환할 Pack
        :type pack: Pack
        :return: 생성된 문자열
        :rtype: str
        """
        result = ''
        index = 0
        while True:
            try:
                line = pack.get_line(Number(index, 1))
            except KeyError:
                break
            line_value = line.expr.eval().value
            if not isinstance(line_value, Number):
                raise RuntimeError("Could not convert it to string, "
                                   "line_value is not a Number: %s" % (
                                       repr(line_value)))
            elif line_value.denominator != 1:
                raise RuntimeError("Could not convert it to string, "
                                   "line_value's denominator is not 1: %s"
                                   % (repr(line_value)))
            result += chr(line_value.numerator)
            index += 1
        return result

    def get_line(self, number):
        """ number를 line number로 가지는 Line을 반환합니다.

        :param number: 가져올 Line의 line number
        :type number: Number
        :return: 해당 Line
        :rtype: Line
        """
        for line in self.line_list.lines:
            ln = line.ln_expr.eval().value
            if not isinstance(ln, Number):
                raise AssertionError("Line numbers must be a Number. %s is "
                                     "not a Number" % (repr(ln),))
            if ln == number:
                return line
        raise KeyError("Cannot found the line")

    def set_line(self, number, value_expr):
        """ number를 line number로 가지는 Line의 expr를 변경합니다.

        :param number: 수정할 Line의 line number
        :type number: Number
        :param value_expr: 수정할 Line의 expr
        :type value_expr: ValueExpr
        :return: NullExpr
        :rtype: NullExpr
        """
        for line in self.line_list.lines:
            ln = line.ln_expr.eval().value
            if not isinstance(ln, Number):
                raise AssertionError("Line numbers must be a Number. %s is "
                                     "not a Number" % (repr(ln),))
            if ln == number:
                line.set_expr(value_expr)
                return NULL_EXPR_INST
        self.line_list.append(Line(ValueExpr(number), value_expr))
        return NULL_EXPR_INST

    def __repr__(self):
        return "{%s}" % (repr(self._line_list),)


class Memory(Pack):
    """ '@' 문자에 매핑되는 특수 Pack class입니다. """

    LN_CURRENT_LINE = Number(0)
    LN_IO = Number(1)

    def __init__(self):
        """ 새로운 Memory을 생성합니다. """
        super().__init__(None)

    def get_line(self, number):
        """ number를 line number로 가지는 Line을 반환합니다.

        만약 number가 LN_IO일 경우, 표준 입력에서 문자열을 가져와 Line의 expr에
        pack으로 변환해 담아서 반환합니다. 모든 입력은 utf-8로 인코딩합니다.

        :param number: 가져올 Line의 line number
        :type number: Number
        :return: 해당 Line
        :rtype: Line
        """
        if number == Memory.LN_IO:
            input_str = io.TextIOWrapper(sys.stdin.buffer,
                                         encoding='utf-8').read()
            return Line(ValueExpr(Memory.LN_IO),
                        ValueExpr(Pack.from_str(input_str)))
        else:
            return super().get_line(number)

    def set_line(self, number, value_expr):
        """ number를 line number로 가지는 Line의 expr를 변경합니다.

        만약 number가 LN_IO일 경우, 표준 출력으로 value_expr의 내용을
        문자열로 변환해 출력합니다.

        :param number: 수정할 Line의 line number
        :type number: Number
        :param value_expr: 수정할 Line의 expr
        :type value_expr: ValueExpr
        :return: NullExpr
        :rtype: NullExpr
        """
        if number == Memory.LN_IO:
            pack_to_print = value_expr.value
            if not isinstance(pack_to_print, Pack):
                raise RuntimeError("Could not print it as string, "
                                   "expr is not a Pack: %s" % (
                                       repr(pack_to_print)))
            print(Pack.to_str(pack_to_print), end='')
            return NULL_EXPR_INST
        else:
            return super().set_line(number, value_expr)

    def __repr__(self):
        return "{" + "".join(repr(line) for line in self.line_list.lines) + "}"


NULL_INST = Null()
NULL_EXPR_INST = ValueExpr(NULL_INST)
MEM = Memory()
