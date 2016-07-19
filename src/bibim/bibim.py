# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from .parser import parser
from .lexer import lexer
from . import datatype
from .io import read_data
from .utils import safe_get_value


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
    datatype.MEM.set_current_noodle_number(datatype.NULL_EXPR_INST)
    current_noodle = get_next_noodle(bowl_inst)
    while current_noodle is not None:
        datatype.MEM.set_current_noodle_number(current_noodle.nn_expr().eval())
        current_noodle.expr().eval()
        current_noodle = get_next_noodle(bowl_inst)


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
        return number.numerator() >= 0
    else:
        return number.gt(current_nn)


def run_file(fp):
    code = read_data(fp)
    os.close(fp)
    bowl = parse(code)
    run(bowl)


def entry_point(argv):
    try:
        filename = argv[1]
    except IndexError:
        print("You must supply a filename")
        return 1

    run_file(os.open(filename, os.O_RDONLY, 0o777))
    return 0
