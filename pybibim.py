import sys
import parser
import lexer
import datatype
from utils import safe_get_value

MODE_NORMAL = 1
MODE_DEBUG = 2

mode = MODE_DEBUG


def parse(code_string):
    """ code_string을 파싱한 결과를 반환합니다.

    :param code_string: parsing할 code 문자열
    :type code_string: str
    :return: 파싱된 결과.
    :rtype: datatime.Value|datatime.Expr|datatime.Line
    """
    return parser.parser.parse(lexer.lexer.lex(code_string))


def run(pack_inst):
    """ pack_inst를 실행합니다.

    :param pack_inst: 실행할 Pack instance
    :type pack_inst: Pack
    """
    if not isinstance(pack_inst, datatype.Pack):
        raise AssertionError('The code must be a Pack.')
    datatype.MEM.set_line(datatype.Memory.LN_CURRENT_LINE,
                          datatype.NULL_EXPR_INST)
    current_line = get_next_line(pack_inst)
    while current_line is not None:
        datatype.MEM.set_line(datatype.Memory.LN_CURRENT_LINE,
                              current_line.ln_expr.eval())
        current_line.expr.eval()
        current_line = get_next_line(pack_inst)


def get_next_line(pack_inst):
    """ pack_inst에서 실행할 다음 Line을 반환합니다.

    다음에 실행할 Line을 발견하지 못하면 None을 반환합니다.

    :param pack_inst: 실행하고 있는 pack instance
    :type pack_inst: Pack
    :return: 다음 line
    :rtype: Line|None
    """
    min_line = None
    min_line_value = None
    for line in pack_inst.line_list.lines:
        ln = safe_get_value(line.ln_expr, datatype.Number)
        if ln is datatype.NULL_INST:
            continue
        if is_nextable_ln(ln):
            if min_line is None or ln < min_line_value:
                min_line = line
                min_line_value = min_line.ln_expr.eval().value
    return min_line


def is_nextable_ln(number):
    """ number가 다음에 실행할 line number가 될 수 있는지 확인합니다.

    마지막에 실행한 line number보다 number가 크면 True를, 작거나 같으면 False를
    반환합니다. 만약 마지막에 실행한 line number가 존재하지 않을 경우에는 number가 0보다
    크거나 같으면 True, 작으면 False를 반환합니다.

    :param number: 확인할 number
    :type number: Number
    :return: 확인 결과
    :rtype: bool
    """
    if number is datatype.NULL_INST:
        return False
    try:
        current_line = datatype.MEM.get_line(datatype.Memory.LN_CURRENT_LINE)
    except KeyError:
        return False
    current_ln = safe_get_value(current_line.expr, datatype.Number)
    if current_ln is datatype.NULL_INST:
        return number.numerator >= 0
    else:
        return number > current_ln


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) != 2:
        print("You must supply a filename")
    filename = argv[1]

    with open(filename, encoding='utf-8') as f:
        code = f.read()
        pack = parse(code)
        run(pack)
