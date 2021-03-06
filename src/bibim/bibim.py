# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from . import datatype, io
from .lexer import lexer
from .parser import parser
from .utils import safe_get_value
from .mode import debug_time, debug_loop


from rpython.rlib.jit import JitDriver

jitdriver = JitDriver(
    greens=[
        'current_noodle',
        'bowl'
    ],
    reds='auto',
    is_recursive=True
)


def parse(code_string):
    """ code_string을 파싱한 결과를 반환합니다.

    :param code_string: parsing할 code 문자열
    :type code_string: str
    :return: 파싱된 결과.
    :rtype: datatime.Value|datatime.Expr|datatime.Noodle
    """
    return parser.parse(lexer.lex(code_string))


def run(bowl_inst):
    """ bowl_inst를 실행합니다.

    :param bowl_inst: 실행할 Bowl instance
    :type bowl_inst: datatime.Bowl
    """
    if not isinstance(bowl_inst, datatype.Bowl):
        raise AssertionError('The code must be a Bowl.')
    mem = datatype.MEM
    mem.set_current_noodle_number(datatype.NULL_EXPR_INST)
    current_noodle = get_next_noodle(bowl_inst)
    while current_noodle is not None:
        jitdriver.jit_merge_point(
            current_noodle=current_noodle,
            bowl=bowl_inst
        )
        current_nn_expr = current_noodle.nn_expr()
        if debug_loop:
            print("Noodle number expression: %s" % current_nn_expr.log_expr())
        current_nn = current_nn_expr.eval()
        if debug_loop:
            print("Noodle number: %s" % current_nn.log_expr())
        mem.set_current_noodle_number(current_nn)
        current_n_expr = current_noodle.expr()
        if debug_loop:
            print("Noodle expression: %s" % current_n_expr.log_expr())
        if debug_loop:
            print("STDIN/OUT start")
        current_n = current_noodle.expr().eval()
        if debug_loop:
            print("\nSTDIN/OUT end")
        if debug_loop:
            print("Noodle expression result: %s" % current_n.log_expr())
        if debug_loop:
            print("Memory: %s" % mem.log_contents())
        current_noodle = get_next_noodle(bowl_inst)
        # raw_input("PRESS ENTER TO CONTINUE.")


def get_next_noodle(bowl_inst):
    """ bowl_inst에서 실행할 다음 Noodle을 반환합니다.

    다음에 실행할 Noodle을 발견하지 못하면 None을 반환합니다.

    :param bowl_inst: 실행하고 있는 Bowl instance
    :type bowl_inst: datatype.Bowl
    :return: 다음 Noodle
    :rtype: datatype.Noodle|None
    """
    min_noodle = None
    min_noodle_value = None
    for noodle in bowl_inst.wad().noodles():
        nn = safe_get_value(noodle.nn_expr(), datatype.Number)
        if nn is datatype.NULL_INST:
            continue
        if is_nextable_nn(nn):
            if min_noodle is None or nn.lt(min_noodle_value):
                min_noodle = noodle
                min_noodle_value = min_noodle.nn_expr().eval().value()
    return min_noodle


def is_nextable_nn(number):
    """ number가 다음에 실행할 noodle number가 될 수 있는지 확인합니다.

    마지막에 실행한 noodle number보다 number가 크면 True를, 작거나 같으면 False를
    반환합니다. 만약 마지막에 실행한 noodle number가 존재하지 않을 경우에는 number가 0보다
    크거나 같으면 True, 작으면 False를 반환합니다.

    :param number: 확인할 number
    :type number: datatype.Number
    :return: 확인 결과
    :rtype: bool
    """
    if number is datatype.NULL_INST:
        return False
    try:
        current_noodle = datatype.MEM.get_noodle(
            datatype.Memory.NN_CURRENT_NOODLE)
    except KeyError:
        return False
    current_nn = safe_get_value(current_noodle.expr(), datatype.Number)
    if current_nn is datatype.NULL_INST:
        return number.numerator().ge(datatype.Number.R_ZERO)
    else:
        return number.gt(current_nn)


def run_file(fp):
    code = io.read_data(fp)
    os.close(fp)
    try:
        bowl = parse(code)
        run(bowl)
    except ValueError as e:
        pass
    except RuntimeError as e:
        pass


def entry_point(argv):
    try:
        filename = argv[1]
    except IndexError:
        print("You must supply a filename")
        return 1

    try:
        fp = os.open(filename, os.O_RDONLY, 0o777)

        if debug_time:
            import time
            start_time = time.time()
            run_file(fp)
            print("runtime: %s sec" % (time.time() - start_time))
        else:
            run_file(fp)
    except OSError as e:
        io.write_data(io.STDOUT, ("Cannot open file %s\n" % (filename,)).decode("utf-8"))
        pass

    return 0
